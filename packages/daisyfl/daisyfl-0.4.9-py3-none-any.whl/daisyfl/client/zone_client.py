import daisyfl as fl
from daisyfl.common import (
    Task,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
    FIT_SAMPLES,
    METRICS,
    LOSS,
    EVALUATE_SAMPLES,
    TID,
)
import argparse
from daisyfl.client.numpy_client import NumPyClient
import threading

# Define Flower Zone client
class ZoneClient(NumPyClient):
    def __init__(self, parent_address, api_ip, api_port, task_manager, cnd_stop):
        self.task_manager = task_manager
        self._cnd_stop: threading.Condition = cnd_stop
        # Start Flower client
        fl.client.start_numpy_client(
            parent_address=parent_address,
            client=self,
            api_ip=api_ip,
            api_port=api_port,
            _zone=True,
        )

    def get_parameters(self, tid: str):
        # return ndarrays
        parameters = self.task_manager.get_parameters(tid=tid)
        return parameters_to_ndarrays(parameters) if parameters is not None else None
        

    def fit(self, parameters, config):
        parameters, report =  self.task_manager.receive_task(parameters=ndarrays_to_parameters(parameters) , task_config=config)
        # return (ndarrays, num_examples, metrics)
        return parameters_to_ndarrays(parameters), report.config[FIT_SAMPLES], report.config

    def evaluate(self, parameters, config):
        _, report =  self.task_manager.receive_task(parameters=ndarrays_to_parameters(parameters) , task_config=config)
        # return "loss, num_examples, metrics"
        return report.config[LOSS], report.config[EVALUATE_SAMPLES], report.config

    def shutdown(self):
        with self._cnd_stop:
            self._cnd_stop.notify()
