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
"""gRPC-based Flower ClientProxy implementation."""

from typing import Optional, Dict, Union, Callable

from daisyfl import common
from daisyfl.common import serde
from daisyfl.proto.transport_pb2 import ClientMessage, ServerMessage
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.server.grpc_server.grpc_bridge import GRPCBridge
from daisyfl.common.logger import log
from logging import WARNING, INFO, ERROR

class GrpcClientProxy(ClientProxy):
    """Flower client proxy which delegates over the network using gRPC."""

    def __init__(
        self,
        cid: str,
        bridge: GRPCBridge,
        metadata_dict: Dict,
    ):
        super().__init__(cid)
        self.bridge = bridge
        self.metadata_dict: Dict = metadata_dict
        self.submit_subtask = None
        self.bridge.set_submit_client_message_fn(self.submit_client_message)

    def get_properties(
        self,
        ins: common.GetPropertiesIns,
    ) -> None:
        """Requests client's set of internal properties."""
        get_properties_msg = serde.get_properties_ins_to_proto(ins)
        self.bridge.request(
            ServerMessage(get_properties_ins=get_properties_msg),
        )

    def get_parameters(
        self,
        ins: common.GetParametersIns,
    ) -> None:
        """Return the current local model parameters."""
        get_parameters_msg = serde.get_parameters_ins_to_proto(ins)
        self.bridge.request(
            ServerMessage(get_parameters_ins=get_parameters_msg),
        )

    def fit(
        self,
        ins: common.FitIns,
    ) -> None:
        """Refine the provided parameters using the locally held dataset."""
        fit_ins_msg = serde.fit_ins_to_proto(ins)
        self.bridge.request(
            ServerMessage(fit_ins=fit_ins_msg),
        )

    def evaluate(
        self,
        ins: common.EvaluateIns,
    ) -> None:
        """Evaluate the provided parameters using the locally held dataset."""
        evaluate_msg = serde.evaluate_ins_to_proto(ins)
        self.bridge.request(
            ServerMessage(evaluate_ins=evaluate_msg),    
        )

    def reconnect(
        self,
        ins: common.ReconnectIns,
    ) -> None:
        """Disconnect and (optionally) reconnect later."""
        reconnect_ins_msg = serde.reconnect_ins_to_proto(ins)
        self.bridge.request(
            ServerMessage(reconnect_ins=reconnect_ins_msg),
        )

    def submit_client_message(
        self, client_message: ClientMessage
    ) -> None:
        field = client_message.WhichOneof("msg")
        if field == "disconnect_res":
            disconnect = serde.disconnect_res_from_proto(client_message.disconnect_res)
            log(INFO, "Will not return {} type of message to Server".format(field))
        elif field == "get_properties_res":
            get_properties_res = serde.get_properties_res_from_proto(client_message.get_properties_res)
            log(INFO, "Will not return {} type of message to Server".format(field))
        elif field == "get_parameters_res":
            get_parameters_res = serde.get_parameters_res_from_proto(client_message.get_parameters_res)
            log(INFO, "Will not return {} type of message to Server".format(field))
        elif field == "fit_res":
            fit_res = serde.fit_res_from_proto(client_message.fit_res)
            self.submit_subtask((self, fit_res))
        elif field == "evaluate_res":
            evaluate_res = serde.evaluate_res_from_proto(client_message.evaluate_res)
            self.submit_subtask((self, evaluate_res))
        else:
            log(INFO, "Will not return {} type of message to Server".format(field))

    def set_submit_subtask_fn(self, submit_subtask: Callable) -> None:
        self.submit_subtask = submit_subtask

