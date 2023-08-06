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
"""Handle server messages by calling appropriate client methods."""


from typing import Tuple

from daisyfl.client.client import (
    Client,
    has_evaluate,
    has_fit,
    has_get_parameters,
    has_get_properties,
)
from daisyfl.client.client_operator_manager import ClientOperatorManager
from daisyfl.common import serde, typing
from daisyfl.common.typing import Parameters
from daisyfl.proto.transport_pb2 import ClientMessage, Reason, ServerMessage

# pylint: disable=missing-function-docstring


class UnknownServerMessage(Exception):
    """Signifies that the received message is unknown."""


_client_operator_manager: ClientOperatorManager = None

def handle(
    server_msg: ServerMessage
) -> ClientMessage:
    """Handle incoming messages from the server.

    Parameters
    ----------
    client : Client
        The Client instance provided by the user.

    Returns
    -------
    client_message: ClientMessage
        The message comming from the server, to be processed by the client.
    sleep_duration : int
        Number of seconds that the client should disconnect from the server.
    keep_going : bool
        Flag that indicates whether the client should continue to process the
        next message from the server (True) or disconnect and optionally
        reconnect later (False).
    """
    field = server_msg.WhichOneof("msg")
    if field == "reconnect_ins":
        return _reconnect(server_msg.reconnect_ins)
    if field == "get_properties_ins":
        return _get_properties(server_msg.get_properties_ins)
    if field == "get_parameters_ins":
        return _get_parameters(server_msg.get_parameters_ins)
    if field == "fit_ins":
        return _fit(server_msg.fit_ins)
    if field == "evaluate_ins":
        return _evaluate(server_msg.evaluate_ins)
    raise UnknownServerMessage()


def _reconnect(
    reconnect_msg: ServerMessage.ReconnectIns,
) -> Tuple[ClientMessage, int]:
    # TODO:
    # Determine the reason for sending DisconnectRes message
    reason = Reason.ACK
    sleep_duration = None
    if reconnect_msg.seconds is not None:
        reason = Reason.RECONNECT
        sleep_duration = reconnect_msg.seconds
    # Build DisconnectRes message
    disconnect_res = ClientMessage.DisconnectRes(reason=reason)

    client_operator_manager = get_client_operator_manager()
    client_operator_manager.disconnect()
    # TODO: reconnect request
    return ClientMessage(disconnect_res=disconnect_res)


def _get_properties(
    get_properties_msg: ServerMessage.GetPropertiesIns
) -> ClientMessage:
    client = get_client_operator_manager().get_client()

    # Check if client overrides get_properties
    if not has_get_properties(client=client):
        # If client does not override get_properties, don't call it
        get_properties_res = typing.GetPropertiesRes(
            status=typing.Status(
                code=typing.Code.GET_PROPERTIES_NOT_IMPLEMENTED,
                message="Client does not implement `get_properties`",
            ),
            properties={},
        )
        get_properties_res_proto = serde.get_properties_res_to_proto(get_properties_res)
        return ClientMessage(get_properties_res=get_properties_res_proto)

    # Deserialize get_properties instruction
    get_properties_ins = serde.get_properties_ins_from_proto(get_properties_msg)
    # Request properties
    get_properties_res = client.get_properties(get_properties_ins)
    # Serialize response
    get_properties_res_proto = serde.get_properties_res_to_proto(get_properties_res)
    return ClientMessage(get_properties_res=get_properties_res_proto)


def _get_parameters(
    get_parameters_msg: ServerMessage.GetParametersIns
) -> ClientMessage:
    client = get_client_operator_manager().get_client()

    # Check if client overrides get_parameters
    if not has_get_parameters(client=client):
        # If client does not override get_parameters, don't call it
        get_parameters_res = typing.GetParametersRes(
            status=typing.Status(
                code=typing.Code.GET_PARAMETERS_NOT_IMPLEMENTED,
                message="Client does not implement `get_parameters`",
            ),
            parameters=Parameters(tensor_type="", tensors=[]),
        )
        get_parameters_res_proto = serde.get_parameters_res_to_proto(get_parameters_res)
        return ClientMessage(get_parameters_res=get_parameters_res_proto)

    # Deserialize get_properties instruction
    get_parameters_ins = serde.get_parameters_ins_from_proto(get_parameters_msg)
    # Request parameters
    get_parameters_res = client.get_parameters(get_parameters_ins)
    # Serialize response
    get_parameters_res_proto = serde.get_parameters_res_to_proto(get_parameters_res)
    return ClientMessage(get_parameters_res=get_parameters_res_proto)


def _fit(fit_msg: ServerMessage.FitIns) -> ClientMessage:
    client_operator_manager = get_client_operator_manager()

    # Deserialize fit instruction
    fit_ins = serde.fit_ins_from_proto(fit_msg)
    # Perform fit
    fit_res = client_operator_manager.fit(fit_ins)
    # Serialize fit result
    fit_res_proto = serde.fit_res_to_proto(fit_res)
    return ClientMessage(fit_res=fit_res_proto)


def _evaluate(evaluate_msg: ServerMessage.EvaluateIns) -> ClientMessage:
    client_operator_manager = get_client_operator_manager()
    
    # Deserialize evaluate instruction
    evaluate_ins = serde.evaluate_ins_from_proto(evaluate_msg)
    # Perform evaluation
    evaluate_res = client_operator_manager.evaluate(evaluate_ins)
    # Serialize evaluate result
    evaluate_res_proto = serde.evaluate_res_to_proto(evaluate_res)
    return ClientMessage(evaluate_res=evaluate_res_proto)


# client_operator_manager
def set_client_operator_manager(client_operator_manager: ClientOperatorManager):
    global _client_operator_manager
    _client_operator_manager = client_operator_manager

def get_client_operator_manager() -> ClientOperatorManager:
    global _client_operator_manager
    return _client_operator_manager
