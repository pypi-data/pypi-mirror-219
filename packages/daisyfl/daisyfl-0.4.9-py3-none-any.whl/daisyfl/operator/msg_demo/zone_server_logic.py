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
from logging import INFO, WARNING, ERROR
from typing import Dict, List, Optional, Tuple, TypedDict, Callable
from threading import Timer, Condition, Event
from queue import Queue
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.operator.strategy import Strategy
from daisyfl.common import (
    Parameters,
    Report,
    Task,
    CURRENT_ROUND,
    TIMEOUT,
    PERIOD,
    CREDENTIAL,
    FitIns,
)
from .msg import (
    TIME,
    Time,
)
from daisyfl.common.logger import log

from daisyfl.operator.utils import (
    get_configure_fit,
    aggregate_fit,
    generate_fit_report,
    get_configure_evaluate,
    aggregate_evaluate,
    generate_evaluate_report,
    wait_for_results,
    get_clients_from_list,
)
from daisyfl.server import Server
from daisyfl.operator.base.server_logic import ServerLogic as BaseServerLogic


class ZoneServerLogic(BaseServerLogic):
    def __init__(self,
        server: Server,
        strategy: Strategy,
    ) -> None:
        self.server: Server = server
        self.strategy: Strategy = strategy

    def fit_round(
        self,
        parameters: Parameters,
        task: Task,
    ) -> Optional[
        Tuple[Optional[Parameters], Optional[Report]]
    ]:
        """Perform a single round fit."""
        stage = Time(task.config[TIME])
        if stage == Time.SAY_HI:
            parameters, report, client_instructions = _say_hi(self, parameters, task,)
            self.clients = client_instructions
            return parameters, report
        elif stage == Time.TRAIN:
            return _fit(self, parameters, task, self.clients)
        else:
            raise ValueError("Invalid stage received")


def _say_hi(
    server_logic: ZoneServerLogic,
    parameters: Parameters,
    task: Task,
) -> Optional[
    Tuple[Optional[Parameters], Optional[Report]]
]:
    ## Get clients and their respective instructions from strategy
    ### credential
    if CREDENTIAL in task.config:
        credential = task.config[CREDENTIAL]
    else:
        log(ERROR, "\"{}\" is a required key in a Task.".format(CREDENTIAL))
    ### get_clients
    client_instructions = get_configure_fit(
        strategy=server_logic.strategy,
        server_round=task.config[CURRENT_ROUND],
        parameters=parameters,
        server=server_logic.server,
        config=task.config,
        credential=credential,
    )
    ## Collect `fit` results from all clients participating in this round
    subtask_id = server_logic.server.fit_clients(
        client_instructions=client_instructions,
        max_workers=server_logic.server.get_max_workers(),
        timeout=task.config[TIMEOUT],
    )
    # check
    success = wait_for_results(strategy=server_logic.strategy, current_returns=server_logic.server.get_current_returns(subtask_id))
    if not success:
        return parameters, generate_fit_report(task.config[CURRENT_ROUND], 0, {},)
    results = server_logic.server.get_results(subtask_id)
    server_logic.server.finish_subtask(subtask_id)
    # Get report
    report = generate_fit_report(
        server_round=task.config[CURRENT_ROUND],
        samples=0,
        metrics_aggregated={},
    )
        
    return parameters, report, client_instructions

def _fit(server_logic: ZoneServerLogic, parameters: Parameters, task: Task, client_instructions: List[Tuple[ClientProxy, FitIns]]):
    """Perform a single round fit."""
    # Get clients and their respective instructions from strategy
    ### credential
    if CREDENTIAL in task.config:
        credential = task.config[CREDENTIAL]
    else:
        log(ERROR, "\"{}\" is a required key in a Task.".format(CREDENTIAL))
    ### get_clients
    client_instructions = get_clients_from_list(server=server_logic.server, clients=client_instructions, timeout=0, credential=credential,)
    client_instructions = get_configure_fit(
        strategy=server_logic.strategy,
        server_round=task.config[CURRENT_ROUND],
        parameters=parameters,
        server=server_logic.server,
        config=task.config,
        credential=credential,
    )
    # Collect `fit` results from all clients participating in this round
    subtask_id = server_logic.server.fit_clients(
        client_instructions=client_instructions,
        max_workers=server_logic.server.get_max_workers(),
        timeout=task.config[TIMEOUT],
    )
    # check
    success = wait_for_results(strategy=server_logic.strategy, current_returns=server_logic.server.get_current_returns(subtask_id))
    if not success:
        return parameters, generate_fit_report(task.config[CURRENT_ROUND], 0, {},)
    results = server_logic.server.get_results(subtask_id)
    server_logic.server.finish_subtask(subtask_id)
    # Aggregate training results
    parameters_aggregated, samples, metrics_aggregated  = aggregate_fit(
        strategy=server_logic.strategy,
        server_round=task.config[CURRENT_ROUND],
        results=results,
        failures=[],
    )
    # Get report
    report = generate_fit_report(
        server_round=task.config[CURRENT_ROUND],
        samples=samples,
        metrics_aggregated=metrics_aggregated,
    )

    return parameters_aggregated, report
