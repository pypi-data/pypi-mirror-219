from logging import DEBUG, INFO, ERROR, WARNING
from queue import Queue
from daisyfl.common.logger import log
from dataclasses import dataclass
from typing import List, Tuple
from daisyfl.utils import dynamic_load
from daisyfl.operator.base.server_logic import ServerLogic
from daisyfl.common import (
    Parameters,
    Task,
    Report,
    TID,
    REMOVE_OPERATOR,
    OPERATORS,
    STRATEGIES,
)
from daisyfl.server.server import Server
from threading import Lock
@dataclass
class TaskOperator:
    tid: str
    operator_path: List[str]
    strategy_path: List[str]
    operator: ServerLogic

class ServerOperatorManager:
    def __init__(self, server: Server):
        self.server: Server = server
        self.operators: List[TaskOperator] = []
    
    def fit_round(self, parameters: Parameters, task: Task) -> Tuple[Parameters, Report]:
        task_operator = self._get_task_operator(tid=task.config[TID])
        if not task_operator:
            self._register_operator(
                tid=task.config[TID],
                operator_path=task.config[OPERATORS][self.operator_key],
                strategy_path=task.config[STRATEGIES][self.strategy_key],
            )
            task_operator = self._get_task_operator(tid=task.config[TID])
        if (task_operator.operator_path != task.config[OPERATORS][self.operator_key]) or \
            (task_operator.strategy_path != task.config[STRATEGIES][self.strategy_key]):
            log(WARNING, "Operator changed.")
            self._unregister_operator(tid=task.config[TID])
            self._register_operator(
                tid=task.config[TID],
                operator_path=task.config[OPERATORS][self.operator_key],
                strategy_path=task.config[STRATEGIES][self.strategy_key],
            )
        parameters, report = task_operator.operator.fit_round(parameters, task,)
        if task.config.__contains__(REMOVE_OPERATOR):
            if task.config[REMOVE_OPERATOR]:
                self._unregister_operator(tid=task.config[TID])
        
        return parameters, report


    def evaluate_round(self, parameters: Parameters, task: Task) -> Report:
        task_operator = self._get_task_operator(tid=task.config[TID])
        if not task_operator:
            self._register_operator(
                tid=task.config[TID],
                operator_path=task.config[OPERATORS][self.operator_key],
                strategy_path=task.config[STRATEGIES][self.strategy_key],
            )
            task_operator = self._get_task_operator(tid=task.config[TID])
        if (task_operator.operator_path != task.config[OPERATORS][self.operator_key]) or \
            (task_operator.strategy_path != task.config[STRATEGIES][self.strategy_key]):
            log(WARNING, "Operator changed.")
            self._unregister_operator(tid=task.config[TID])
            self._register_operator(
                tid=task.config[TID],
                operator_path=task.config[OPERATORS][self.operator_key],
                strategy_path=task.config[STRATEGIES][self.strategy_key],
            )
        report = task_operator.operator.evaluate_round(parameters, task,)
        if task.config.__contains__(REMOVE_OPERATOR):
            if task.config[REMOVE_OPERATOR]:
                self._unregister_operator(tid=task.config[TID])
        
        return report
    

    # called by task_manager
    def set_operator_key(self, keys: List[str]) -> None:
        self.operator_key = keys[0]
        self.strategy_key = keys[1]

    def _get_task_operator(self, tid: str) -> TaskOperator:
        for task_operator in self.operators:
            if task_operator.tid == tid:
                return task_operator
        return None
    
    def _register_operator(self,
        tid: str,
        operator_path: List[str],
        strategy_path: List[str],
    ) -> bool:
        if self._get_task_operator(tid=tid):
            return False
        operator: ServerLogic = dynamic_load(operator_path[0], operator_path[1])
        strategy = dynamic_load(strategy_path[0], strategy_path[1])
        self.operators.append(TaskOperator(
            tid=tid,
            operator_path=operator_path,
            strategy_path=strategy_path,
            operator=operator(server=self.server, strategy=strategy(),),
        ))
        return True
    
    def _unregister_operator(self, tid: str) -> bool:
        for i in range(len(self.operators)):
            if self.operators[i].tid == tid:
                del self.operators[i]
                return True
        return False

