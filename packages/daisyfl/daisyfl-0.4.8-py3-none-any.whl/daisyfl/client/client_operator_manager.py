from logging import DEBUG, INFO, ERROR, WARNING
from daisyfl.common.logger import log
from dataclasses import dataclass
from typing import List, Tuple
from daisyfl.utils import dynamic_load
from daisyfl.operator.base.client_logic import ClientLogic
from daisyfl.common import (
    Parameters,
    Task,
    Report,
    FitIns,
    FitRes,
    EvaluateIns,
    EvaluateRes,
    TID,
    REMOVE_OPERATOR,
    OPERATORS,
    STRATEGIES,
)

from daisyfl.client.client import Client

@dataclass
class TaskOperator:
    tid: str
    operator_path: List[str]
    operator: ClientLogic


class ClientOperatorManager:
    def __init__(self, client: Client):
        self.client: Client = client
        self.operators: List[TaskOperator] = []

    def disconnect(self) -> None:
        # TODO:
        pass

    def fit(
        self, ins: FitIns,
    ) -> FitRes:
        task_operator = self._get_task_operator(tid=ins.config[TID])
        if not task_operator:
            self._register_operator(
                tid=ins.config[TID],
                operator_path=ins.config[OPERATORS][self.operator_key],
            )
            task_operator = self._get_task_operator(tid=ins.config[TID])
        if (task_operator.operator_path != ins.config[OPERATORS][self.operator_key]):
            log(WARNING, "Operator changed.")
            self._unregister_operator(tid=ins.config[TID])
            self._register_operator(
                tid=ins.config[TID],
                operator_path=ins.config[OPERATORS][self.operator_key],
            )

        res: FitRes = task_operator.operator.fit(ins)

        if ins.config.__contains__(REMOVE_OPERATOR):
            if ins.config[REMOVE_OPERATOR]:
                self._unregister_operator(tid=ins.config[TID])

        return res

    def evaluate(
        self, ins: EvaluateIns,
    ) -> EvaluateRes:
        task_operator = self._get_task_operator(tid=ins.config[TID])

        if not task_operator:
            self._register_operator(
                tid=ins.config[TID],
                operator_path=ins.config[OPERATORS][self.operator_key],
            )
            task_operator = self._get_task_operator(tid=ins.config[TID])
        if (task_operator.operator_path != ins.config[OPERATORS][self.operator_key]):
            log(WARNING, "Operator changed.")
            self._unregister_operator(tid=ins.config[TID])
            self._register_operator(
                tid=ins.config[TID],
                operator_path=ins.config[OPERATORS][self.operator_key],
            )

        res: FitRes = task_operator.operator.evaluate(ins)
        
        if ins.config.__contains__(REMOVE_OPERATOR):
            if ins.config[REMOVE_OPERATOR]:
                self._unregister_operator(tid=ins.config[TID])

        return res 

    # called by client.app
    def set_operator_key(self, key: str) -> None:
        self.operator_key = key

    def _get_task_operator(self, tid: str) -> TaskOperator:
        for task_operator in self.operators:
            if task_operator.tid == tid:
                return task_operator
        return None
    
    def _register_operator(self,
        tid: str,
        operator_path: List[str],
    ) -> bool:
        if self._get_task_operator(tid=tid):
            return False

        operator: ClientLogic = dynamic_load(operator_path[0], operator_path[1])

        self.operators.append(TaskOperator(
            tid=tid,
            operator_path=operator_path,
            operator=operator(client=self.client)
        ))

        return True
    
    def _unregister_operator(self, tid: str) -> bool:
        for i in range(len(self.operators)):
            if self.operators[i].tid == tid:
                del self.operators[i]
                return True
        return False

