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
"""ProtoBuf serialization and deserialization."""


from typing import Any, List, cast

from daisyfl.proto.transport_pb2 import (
    ClientMessage,
    Code,
    Element,
    Parameters,
    Reason,
    Scalar,
    ServerMessage,
    Status,
    InnerMap,
    InnerMapInt,
    InnerList,
)

from . import typing

# pylint: disable=missing-function-docstring


def parameters_to_proto(parameters: typing.Parameters) -> Parameters:
    """."""
    return Parameters(tensors=parameters.tensors, tensor_type=parameters.tensor_type)


def parameters_from_proto(msg: Parameters) -> typing.Parameters:
    """."""
    tensors: List[bytes] = list(msg.tensors)
    return typing.Parameters(tensors=tensors, tensor_type=msg.tensor_type)


#  === ReconnectIns message ===


def reconnect_ins_to_proto(ins: typing.ReconnectIns) -> ServerMessage.ReconnectIns:
    """Serialize ReconnectIns to ProtoBuf message."""
    if ins.seconds is not None:
        return ServerMessage.ReconnectIns(seconds=ins.seconds)
    return ServerMessage.ReconnectIns()


def reconnect_ins_from_proto(msg: ServerMessage.ReconnectIns) -> typing.ReconnectIns:
    """Deserialize ReconnectIns from ProtoBuf message."""
    return typing.ReconnectIns(seconds=msg.seconds)


# === DisconnectRes message ===


def disconnect_res_to_proto(res: typing.DisconnectRes) -> ClientMessage.DisconnectRes:
    """Serialize DisconnectRes to ProtoBuf message."""
    reason_proto = Reason.UNKNOWN
    if res.reason == "RECONNECT":
        reason_proto = Reason.RECONNECT
    elif res.reason == "POWER_DISCONNECTED":
        reason_proto = Reason.POWER_DISCONNECTED
    elif res.reason == "WIFI_UNAVAILABLE":
        reason_proto = Reason.WIFI_UNAVAILABLE
    return ClientMessage.DisconnectRes(reason=reason_proto)


def disconnect_res_from_proto(msg: ClientMessage.DisconnectRes) -> typing.DisconnectRes:
    """Deserialize DisconnectRes from ProtoBuf message."""
    if msg.reason == Reason.RECONNECT:
        return typing.DisconnectRes(reason="RECONNECT")
    if msg.reason == Reason.POWER_DISCONNECTED:
        return typing.DisconnectRes(reason="POWER_DISCONNECTED")
    if msg.reason == Reason.WIFI_UNAVAILABLE:
        return typing.DisconnectRes(reason="WIFI_UNAVAILABLE")
    return typing.DisconnectRes(reason="UNKNOWN")


# === GetParameters messages ===


def get_parameters_ins_to_proto(
    ins: typing.GetParametersIns,
) -> ServerMessage.GetParametersIns:
    """Serialize GetParametersIns to ProtoBuf message."""
    config = properties_to_proto(ins.config)
    return ServerMessage.GetParametersIns(config=config)


def get_parameters_ins_from_proto(
    msg: ServerMessage.GetParametersIns,
) -> typing.GetParametersIns:
    """Deserialize GetParametersIns from ProtoBuf message."""
    config = properties_from_proto(msg.config)
    return typing.GetParametersIns(config=config)


def get_parameters_res_to_proto(
    res: typing.GetParametersRes,
) -> ClientMessage.GetParametersRes:
    """."""
    status_msg = status_to_proto(res.status)
    if res.status.code == typing.Code.GET_PARAMETERS_NOT_IMPLEMENTED:
        return ClientMessage.GetParametersRes(status=status_msg)
    parameters_proto = parameters_to_proto(res.parameters)
    return ClientMessage.GetParametersRes(
        status=status_msg, parameters=parameters_proto
    )


def get_parameters_res_from_proto(
    msg: ClientMessage.GetParametersRes,
) -> typing.GetParametersRes:
    """."""
    status = status_from_proto(msg=msg.status)
    parameters = parameters_from_proto(msg.parameters)
    return typing.GetParametersRes(status=status, parameters=parameters)


# === Fit messages ===


def fit_ins_to_proto(ins: typing.FitIns) -> ServerMessage.FitIns:
    """Serialize FitIns to ProtoBuf message."""
    parameters_proto = parameters_to_proto(ins.parameters)
    config_msg = inner_map_to_proto(ins.config)
    return ServerMessage.FitIns(parameters=parameters_proto, config=config_msg)


def fit_ins_from_proto(msg: ServerMessage.FitIns) -> typing.FitIns:
    """Deserialize FitIns from ProtoBuf message."""
    parameters = parameters_from_proto(msg.parameters)
    config = inner_map_from_proto(msg.config)
    return typing.FitIns(parameters=parameters, config=config)


def fit_res_to_proto(res: typing.FitRes) -> ClientMessage.FitRes:
    """Serialize FitIns to ProtoBuf message."""
    status_msg = status_to_proto(res.status)
    if res.status.code == typing.Code.FIT_NOT_IMPLEMENTED:
        return ClientMessage.FitRes(status=status_msg)
    parameters_proto = parameters_to_proto(res.parameters)
    config_msg = None if res.config is None else inner_map_to_proto(res.config)
    return ClientMessage.FitRes(
        status=status_msg,
        parameters=parameters_proto,
        config=config_msg,
    )


def fit_res_from_proto(msg: ClientMessage.FitRes) -> typing.FitRes:
    """Deserialize FitRes from ProtoBuf message."""
    status = status_from_proto(msg=msg.status)
    parameters = parameters_from_proto(msg.parameters)
    config = None if msg.config is None else inner_map_from_proto(msg.config)
    return typing.FitRes(
        status=status,
        parameters=parameters,
        config=config,
    )


# === Properties messages ===


def get_properties_ins_to_proto(
    ins: typing.GetPropertiesIns,
) -> ServerMessage.GetPropertiesIns:
    """Serialize GetPropertiesIns to ProtoBuf message."""
    config = properties_to_proto(ins.config)
    return ServerMessage.GetPropertiesIns(config=config)


def get_properties_ins_from_proto(
    msg: ServerMessage.GetPropertiesIns,
) -> typing.GetPropertiesIns:
    """Deserialize GetPropertiesIns from ProtoBuf message."""
    config = properties_from_proto(msg.config)
    return typing.GetPropertiesIns(config=config)


def get_properties_res_to_proto(
    res: typing.GetPropertiesRes,
) -> ClientMessage.GetPropertiesRes:
    """Serialize GetPropertiesIns to ProtoBuf message."""
    status_msg = status_to_proto(res.status)
    if res.status.code == typing.Code.GET_PROPERTIES_NOT_IMPLEMENTED:
        return ClientMessage.GetPropertiesRes(status=status_msg)
    properties_msg = properties_to_proto(res.properties)
    return ClientMessage.GetPropertiesRes(status=status_msg, properties=properties_msg)


def get_properties_res_from_proto(
    msg: ClientMessage.GetPropertiesRes,
) -> typing.GetPropertiesRes:
    """Deserialize GetPropertiesRes from ProtoBuf message."""
    status = status_from_proto(msg=msg.status)
    properties = properties_from_proto(msg.properties)
    return typing.GetPropertiesRes(status=status, properties=properties)


def status_to_proto(status: typing.Status) -> Status:
    """Serialize Code to ProtoBuf message."""
    code = Code.OK
    if status.code == typing.Code.GET_PROPERTIES_NOT_IMPLEMENTED:
        code = Code.GET_PROPERTIES_NOT_IMPLEMENTED
    if status.code == typing.Code.GET_PARAMETERS_NOT_IMPLEMENTED:
        code = Code.GET_PARAMETERS_NOT_IMPLEMENTED
    if status.code == typing.Code.FIT_NOT_IMPLEMENTED:
        code = Code.FIT_NOT_IMPLEMENTED
    if status.code == typing.Code.EVALUATE_NOT_IMPLEMENTED:
        code = Code.EVALUATE_NOT_IMPLEMENTED
    if status.code == typing.Code.MESSAGE_LOST:
        code = Code.MESSAGE_LOST
    return Status(code=code, message=status.message)


def status_from_proto(msg: Status) -> typing.Status:
    """Deserialize Code from ProtoBuf message."""
    code = typing.Code.OK
    if msg.code == Code.GET_PROPERTIES_NOT_IMPLEMENTED:
        code = typing.Code.GET_PROPERTIES_NOT_IMPLEMENTED
    if msg.code == Code.GET_PARAMETERS_NOT_IMPLEMENTED:
        code = typing.Code.GET_PARAMETERS_NOT_IMPLEMENTED
    if msg.code == Code.FIT_NOT_IMPLEMENTED:
        code = typing.Code.FIT_NOT_IMPLEMENTED
    if msg.code == Code.EVALUATE_NOT_IMPLEMENTED:
        code = typing.Code.EVALUATE_NOT_IMPLEMENTED
    if msg.code == Code.MESSAGE_LOST:
        code = typing.Code.MESSAGE_LOST
    return typing.Status(code=code, message=msg.message)


# === Evaluate messages ===


def evaluate_ins_to_proto(ins: typing.EvaluateIns) -> ServerMessage.EvaluateIns:
    """Serialize EvaluateIns to ProtoBuf message."""
    parameters_proto = parameters_to_proto(ins.parameters)
    config_msg = inner_map_to_proto(ins.config)
    return ServerMessage.EvaluateIns(parameters=parameters_proto, config=config_msg)


def evaluate_ins_from_proto(msg: ServerMessage.EvaluateIns) -> typing.EvaluateIns:
    """Deserialize EvaluateIns from ProtoBuf message."""
    parameters = parameters_from_proto(msg.parameters)
    config = inner_map_from_proto(msg.config)
    return typing.EvaluateIns(parameters=parameters, config=config)


def evaluate_res_to_proto(res: typing.EvaluateRes) -> ClientMessage.EvaluateRes:
    """Serialize EvaluateIns to ProtoBuf message."""
    status_msg = status_to_proto(res.status)
    if res.status.code == typing.Code.EVALUATE_NOT_IMPLEMENTED:
        return ClientMessage.EvaluateRes(status=status_msg)
    config_msg = None if res.config is None else inner_map_to_proto(res.config)
    return ClientMessage.EvaluateRes(
        status=status_msg,
        config=config_msg,
    )


def evaluate_res_from_proto(msg: ClientMessage.EvaluateRes) -> typing.EvaluateRes:
    """Deserialize EvaluateRes from ProtoBuf message."""
    status = status_from_proto(msg=msg.status)
    config = None if msg.config is None else inner_map_from_proto(msg.config)
    return typing.EvaluateRes(
        status=status,
        config=config,
    )


#  === ClientStatus ===


def client_status_to_proto(res: typing.ClientStatus) -> ClientMessage.ClientStatus:
    """Serialize ClientStatus to ProtoBuf message."""
    return ClientMessage.ClientStatus(status=res.status)


def client_status_from_proto(msg: ClientMessage.ClientStatus) -> typing.ClientStatus:
    """Deserialize ProtoBuf message to ClientStatus."""
    return typing.ClientStatus(status=msg.status)


# === SRS, CRS ===


def server_received_signal_to_proto(ins: typing.ServerReceivedSignal) -> ServerMessage.ServerReceivedSignal:
    """Serialize SRS to ProtoBuf message."""
    status_proto = status_to_proto(ins.status)
    return ServerMessage.ServerReceivedSignal(status=status_proto)


def server_received_signal_from_proto(msg: ServerMessage.ServerReceivedSignal) -> typing.ServerReceivedSignal:
    """Deserialize ProtoBug message to SRS"""
    status = status_from_proto(msg.status)
    return typing.ServerReceivedSignal(status=status)


def client_received_signal_to_proto(res: typing.ClientReceivedSignal) -> ClientMessage.ClientReceivedSignal:
    """Serialize CRS to ProtoBuf message."""
    status_proto = status_to_proto(res.status)
    return ClientMessage.ClientReceivedSignal(status=status_proto)


def client_received_signal_from_proto(msg: ClientMessage.ClientReceivedSignal) -> typing.ClientReceivedSignal:
    """Deserialize ProtoBug message to CRS"""
    status = status_from_proto(msg.status)
    return typing.ClientReceivedSignal(status=status)


# === Properties messages ===


def properties_to_proto(properties: typing.Properties) -> Any:
    """Serialize... ."""
    proto = {}
    for key in properties:
        proto[key] = scalar_to_proto(properties[key])
    return proto


def properties_from_proto(proto: Any) -> typing.Properties:
    """Deserialize... ."""
    properties = {}
    for k in proto:
        properties[k] = scalar_from_proto(proto[k])
    return properties


# === Element messages ===


def element_to_proto(element: typing.Element) -> Element:

    if isinstance(element, bool):
        return Element(bool=element)

    if isinstance(element, bytes):
        return Element(bytes=element)

    if isinstance(element, float):
        return Element(double=element)

    if isinstance(element, int):
        return Element(sint64=element)

    if isinstance(element, str):
        return Element(string=element)
    
    if (isinstance(element, dict)):
        keys = list(element.keys())
        if len(keys) > 0 and type(keys[0]) == int:
            return Element(inner_map_int=inner_map_int_to_proto(element))
        return Element(inner_map=inner_map_to_proto(element))
    
    if (isinstance(element, List)):
        return Element(inner_list=inner_list_to_proto(element))

    raise Exception(
        f"Accepted types: {bool, bytes, float, int, str, dict, List} (but not {type(element)})"
    )


def element_from_proto(element_msg: Element) -> typing.Element:
    """Deserialize... ."""
    element_field = element_msg.WhichOneof("element")
    element = getattr(element_msg, cast(str, element_field))
    if type(cast(typing.Element, element)) is InnerMap:
        inner_map_msg = cast(typing.Element, element)
        return inner_map_from_proto(inner_map_msg)
    elif type(cast(typing.Element, element)) is InnerMapInt:
        inner_map_int_msg = cast(typing.Element, element)
        return inner_map_int_from_proto(inner_map_int_msg)
    elif type(cast(typing.Element, element)) is InnerList:
        inner_list_msg = cast(typing.Element, element)
        return inner_list_from_proto(inner_list_msg)
    return cast(typing.Element, element)


# DEBUG: it goes failed if multiple key types in a dictionary
# === InnerMap messages ===


def inner_map_to_proto(inner_map: Any) -> InnerMap:
    """Serialize... ."""
    proto = {}
    for key in inner_map:
        proto[key] = element_to_proto(inner_map[key])
    return InnerMap(inner_map=proto)


def inner_map_from_proto(inner_map_msg: InnerMap) -> Any:
    """Deserialize... ."""
    inner_map_field = cast(str, InnerMap.DESCRIPTOR.fields[0].name)
    proto = getattr(inner_map_msg, inner_map_field)
    inner_map = {}
    for key in proto:
        inner_map[key] = element_from_proto(proto[key])
    return inner_map


# DEBUG: it goes failed if multiple key types in a dictionary
# === InnerMapInt messages ===


def inner_map_int_to_proto(inner_map_int: Any) -> InnerMapInt:
    """Serialize... ."""
    proto = {}
    for key in inner_map_int:
        proto[key] = element_to_proto(inner_map_int[key])
    return InnerMapInt(inner_map_int=proto)


def inner_map_int_from_proto(inner_map_int_msg: InnerMapInt) -> Any:
    """Deserialize... ."""
    inner_map_int_field = cast(str, InnerMapInt.DESCRIPTOR.fields[0].name)
    proto = getattr(inner_map_int_msg, inner_map_int_field)
    inner_map_int = {}
    for key in proto:
        inner_map_int[key] = element_from_proto(proto[key])
    return inner_map_int


# === InnerList messages ===


def inner_list_to_proto(inner_list: Any) -> InnerMap:
    """Serialize... ."""
    proto = []
    for i in range(len(inner_list)):
        proto.append(element_to_proto(inner_list[i]))
    return InnerList(inner_list=proto)


def inner_list_from_proto(inner_list_msg: InnerList) -> Any:
    """Deserialize... ."""
    inner_list_field = cast(str, InnerList.DESCRIPTOR.fields[0].name)
    proto = getattr(inner_list_msg, inner_list_field)
    inner_list = []
    for i in range(len(proto)):
        inner_list.append(element_from_proto(proto[i]))
    return inner_list


# === Metrics messages ===


def metrics_to_proto(metrics: typing.Metrics) -> Any:
    """Serialize... ."""
    proto = {}
    for key in metrics:
        proto[key] = scalar_to_proto(metrics[key])
    return proto


def metrics_from_proto(proto: Any) -> typing.Metrics:
    """Deserialize... ."""
    metrics = {}
    for k in proto:
        metrics[k] = scalar_from_proto(proto[k])
    return metrics


# === Scalar messages ===


def scalar_to_proto(scalar: typing.Scalar) -> Scalar:
    """Serialize... ."""

    if isinstance(scalar, bool):
        return Scalar(bool=scalar)

    if isinstance(scalar, bytes):
        return Scalar(bytes=scalar)

    if isinstance(scalar, float):
        return Scalar(double=scalar)

    if isinstance(scalar, int):
        return Scalar(sint64=scalar)

    if isinstance(scalar, str):
        return Scalar(string=scalar)

    raise Exception(
        f"Accepted types: {bool, bytes, float, int, str} (but not {type(scalar)})"
    )


def scalar_from_proto(scalar_msg: Scalar) -> typing.Scalar:
    """Deserialize... ."""
    scalar_field = scalar_msg.WhichOneof("scalar")
    scalar = getattr(scalar_msg, cast(str, scalar_field))
    return cast(typing.Scalar, scalar)
    