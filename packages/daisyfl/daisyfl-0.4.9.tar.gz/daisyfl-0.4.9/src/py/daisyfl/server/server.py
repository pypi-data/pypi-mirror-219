# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower server."""


import concurrent.futures
import timeit
from threading import Event, Condition, Lock, Timer
from queue import Queue
from logging import DEBUG, INFO
from typing import Dict, List, Optional, Tuple, Union, Callable
import gc
from daisyfl.common import (
    Task,
    Report,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    Code,
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    ReconnectIns,
    Scalar,
    CurrentReturns,
    CID,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import GetParametersIns
from daisyfl.server.client_manager import ClientManager
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.server.history import History

FitResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, FitRes]],
    List[Union[Tuple[ClientProxy, FitRes], BaseException]],
]
EvaluateResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, EvaluateRes]],
    List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
]
ReconnectResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, DisconnectRes]],
    List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]],
]

# TODO: selection: master knows how many clients are selected (bug: wait_for_sync)
# TODO: update CurrentReturns by number of client

class SubtaskManager:
    def __init__(self,) -> None:
        self.subtasks: Dict[int, CurrentReturns] = {}
        self.queues: Dict[int, Queue] = {}
        self.client_previous_subtask: Dict[str, int] = {}
        self._lock: Lock = Lock()
        self._subtask_num = 0
    
    def subtask_id_generator(self,) -> int:
        with self._lock:
            tmp = self._subtask_num
            self._subtask_num += 1
        return tmp
    
    def register_subtask(
        self, subtask_id: int, 
        client_instructions: List[Tuple[ClientProxy, FitIns]],
        timeout: int,
    ) -> None:
        # CurrentReturns
        self.subtasks[subtask_id]: CurrentReturns = CurrentReturns(
            selected=len(client_instructions),
            results_num=0,
            failures_num=0,
            cnd=Condition(),
        )
        # queue
        self.queues[subtask_id] = Queue()
        # update client_previoud_subtask
        for item in client_instructions:
            cid = item[0].cid
            if self.client_previous_subtask.__contains__(cid):
                pre_subtask = self.client_previous_subtask[cid]
                self.subtasks[pre_subtask].failures_num += 1
                del self.client_previous_subtask[cid]
                self.subtasks[pre_subtask].cnd.notify_all()
            self.client_previous_subtask[cid] = subtask_id
        # timeout
        Timer(timeout, self.subtask_timeout, subtask_id)

    def unregister_subtask(self, subtask_id: int) -> None:
        del self.subtasks[subtask_id]
        del self.queues[subtask_id]
        cid_list = list(self.client_previous_subtask.keys())
        for cid in cid_list:
            if self.client_previous_subtask[cid] == subtask_id:
                del self.client_previous_subtask[cid]
        gc.collect()
        return

    def submit_subtask(
        self, result: Tuple[ClientProxy, Union[FitRes, EvaluateRes]],
    ) -> None:
        client_proxy, res = result
        if (not self.client_previous_subtask.__contains__(client_proxy.cid)):
            return
        subtask_id = self.client_previous_subtask[client_proxy.cid]
        if (not self.subtasks.__contains__(subtask_id)):
            return
        # Check result status code
        if res.status.code == Code.OK:
            result[1].config[CID] = result[0].cid
            self.subtasks[subtask_id].results_num += 1
            self.queues[subtask_id].put(result)
        # Not successful, client returned a result where the status code is not OK
        else:
            self.subtasks[subtask_id].failures_num += 1
        del self.client_previous_subtask[client_proxy.cid]
        with self.subtasks[subtask_id].cnd:
            self.subtasks[subtask_id].cnd.notify_all()
        return
        
    def get_current_returns(self, subtask_id: int) -> CurrentReturns:
        return self.subtasks[subtask_id]
    
    def get_results(self, subtask_id: int) -> List[Tuple[ClientProxy, Union[FitRes, EvaluateRes]]]:
        results = []
        q = self.queues[subtask_id]
        for _ in range(q.qsize()):
            results.append(q.get())
        return results
      
    def subtask_timeout(self, substask_id: int,) -> None:
        if self.subtasks.__contains__(substask_id):
            self.unregister_subtask(substask_id)


class Server:
    """Flower server."""
    def __init__(
        self, *, 
        client_manager: ClientManager,
    ) -> None:
        self._client_manager: ClientManager = client_manager
        self._max_workers: Optional[int] = None
        self._subtask_manager: SubtaskManager = SubtaskManager()
        self._client_manager.set_submit_subtask_fn(self._subtask_manager.submit_subtask)

    # set Server attributes
    def set_max_workers(self, max_workers: Optional[int]) -> None:
        """Set the max_workers used by ThreadPoolExecutor."""
        self._max_workers = max_workers

    # get Server attributes
    def get_client_manager(self) -> ClientManager:
        """Return ClientManager."""
        return self._client_manager

    def get_max_workers(self) -> Optional[int]:
        """Return max_workers."""
        return self._max_workers
    
    # NOTE: ClientManager APIs 
    def num_available(self, credential: Optional[str] = None) -> int:
        return self._client_manager.num_available(credential=credential)
        
    def get_available_clients(
        self,
        min_num_clients: int = 2,
        credential: Optional[str] = None,
    ) -> List[ClientProxy]:
        return self._client_manager.get_available_clients(
            min_num_clients=min_num_clients,
            credential=credential,
        )
    
    def get_clients_from_list(
        self,
        clients: List[Tuple[ClientProxy, Union[FitIns, EvaluateIns]]],
        timeout: float,
        credential: str,
    ) -> List[Tuple[ClientProxy, Union[FitIns, EvaluateIns]]]:
        ids = []
        client_list = []
        instructions = []
        for client, ins in clients:
            ids.append(client.cid)
            client_list.append(client)
            instructions.append(ins)
        client_list = self._client_manager.get_clients_from_list(clients=client_list, timeout=timeout, credential=credential,)
        available_clients_and_ins = []
        for client in client_list:
            available_clients_and_ins.append((client, instructions[ids.index(client.cid)]))
        return available_clients_and_ins

    # NOTE: SubtaskManager APIs
    def finish_subtask(self, subtask_id: int) -> None:
        self._subtask_manager.unregister_subtask(subtask_id)

    def get_current_returns(self, subtask_id: int) -> CurrentReturns:
        return self._subtask_manager.get_current_returns(subtask_id)
    
    def get_results(self, subtask_id: int) -> List[Tuple[ClientProxy, Union[FitRes, EvaluateRes]]]:
        return self._subtask_manager.get_results(subtask_id)

    # TODO:
    def disconnect_all_clients(self,) -> None:
        """Send shutdown signal to all clients."""
        clients = self.get_client_manager().all() 
        instruction = ReconnectIns(seconds=None)
        client_instructions = [(client_proxy, instruction) for client_proxy in clients]
        _ = self._reconnect_clients(
            client_instructions=client_instructions,
            max_workers=self.get_max_workers(),
        )

    def fit_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, FitIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
    ) -> int:
        subtask_id = self._subtask_manager.subtask_id_generator()
        self._subtask_manager.register_subtask(subtask_id, client_instructions, timeout)
        self._fit_clients(
            client_instructions=client_instructions,
            max_workers=max_workers,
        )
        return subtask_id
    
    def evaluate_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, EvaluateIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
    ) -> int:
        subtask_id = self._subtask_manager.subtask_id_generator()
        self._subtask_manager.register_subtask(subtask_id, client_instructions, timeout)
        self._evaluate_clients(
            client_instructions=client_instructions,
            max_workers=max_workers,
        )
        return subtask_id


    def _reconnect_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, ReconnectIns]],
        max_workers: Optional[int],
    ) -> ReconnectResultsAndFailures:
        """Instruct clients to disconnect and never reconnect."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            submitted_fs = {
                executor.submit(self._reconnect_client, self, client_proxy, ins,)
                for client_proxy, ins in client_instructions
            }
            finished_fs, _ = concurrent.futures.wait(
                fs=submitted_fs,
                timeout=None,  # Handled in the respective communication stack
            )

        # Gather results
        results: List[Tuple[ClientProxy, DisconnectRes]] = []
        failures: List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]] = []
        for future in finished_fs:
            failure = future.exception()
            if failure is not None:
                failures.append(failure)
            else:
                result = future.result()
                results.append(result)
        return results, failures


    def _reconnect_client(
        self,
        client: ClientProxy,
        reconnect: ReconnectIns,
        timeout: Optional[float],
    ) -> Tuple[ClientProxy, DisconnectRes]:
        """Instruct client to disconnect and (optionally) reconnect later."""
        disconnect = client.reconnect(
            reconnect,
            timeout=timeout,
        )
        return client, disconnect


    def _fit_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, FitIns]],
        max_workers: Optional[int],
    ) -> None:
        """Refine parameters concurrently on all selected clients."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            {
                executor.submit(client_proxy.fit, ins,)
                for client_proxy, ins in client_instructions
            }


    def _evaluate_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, EvaluateIns]],
        max_workers: Optional[int],
    ) -> None:
        """Evaluate parameters concurrently on all selected clients."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            {
                executor.submit(client_proxy.evaluate, ins,)
                for client_proxy, ins in client_instructions
            }

