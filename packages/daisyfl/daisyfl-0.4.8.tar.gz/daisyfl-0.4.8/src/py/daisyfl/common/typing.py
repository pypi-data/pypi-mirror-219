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
"""Flower type definitions."""


from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, TypedDict
from threading import Condition
import numpy.typing as npt

NDArray = npt.NDArray[Any]
NDArrays = List[NDArray]

# The following union type contains Python types corresponding to ProtoBuf types that
# ProtoBuf considers to be "Scalar Value Types", even though some of them arguably do
# not conform to other definitions of what a scalar is. Source:
# https://developers.google.com/protocol-buffers/docs/overview#scalar
Scalar = Union[bool, bytes, float, int, str]
# TODO: replace "Metrics" with an appropriate name
Metrics = Dict[str, Scalar]

Element = Union[Scalar, Dict, None]

MetricsAggregationFn = Callable[[List[Tuple[int, Metrics]]], Metrics]

Properties = Dict[str, Scalar]


class Code(Enum):
    """Client status codes."""

    OK = 0
    GET_PROPERTIES_NOT_IMPLEMENTED = 1
    GET_PARAMETERS_NOT_IMPLEMENTED = 2
    FIT_NOT_IMPLEMENTED = 3
    EVALUATE_NOT_IMPLEMENTED = 4
    MESSAGE_LOST = 5


@dataclass
class Status:
    """Client status."""

    code: Code
    message: str


@dataclass
class Parameters:
    """Model parameters."""

    tensors: List[bytes]
    tensor_type: str


@dataclass
class GetParametersIns:
    """Parameters request for a client."""

    config: Dict[str, Scalar]

@dataclass
class GetParametersRes:
    """Response when asked to return parameters."""

    status: Status
    parameters: Parameters


@dataclass
class FitIns:
    """Fit instructions for a client."""

    parameters: Parameters
    config: TypedDict


@dataclass
class FitRes:
    """Fit response from a client."""

    status: Status
    parameters: Parameters
    config: TypedDict


@dataclass
class EvaluateIns:
    """Evaluate instructions for a client."""

    parameters: Parameters
    config: TypedDict


@dataclass
class EvaluateRes:
    """Evaluate response from a client."""

    status: Status
    config: TypedDict


@dataclass
class GetPropertiesIns:
    """Properties request for a client."""

    config: Dict[str, Scalar]


@dataclass
class GetPropertiesRes:
    """Properties response from a client."""

    status: Status
    properties: Properties


@dataclass
class ReconnectIns:
    """ReconnectIns message from server to client."""

    seconds: Optional[int]


@dataclass
class DisconnectRes:
    """DisconnectRes message from client to server."""

    reason: str

@dataclass
class Task:
    """Input a task when calling server API."""
    config: TypedDict
    # TID: str
    # NUM_ROUNDS: int
    # CURRENT_ROUND: int
    # EVALUATE: bool
    # TIMEOUT: int


@dataclass
class Report:
    """After complete a task, return a report."""
    config: TypedDict
    # CURRENT_ROUND: int
    # FIT_SAMPLES: int
    # EVALUATE_SAMPLES: int
    # LOSS: float
    # METRICS: Metrics

class Type(Enum):
    """Type of the task manager."""
    
    MASTER = 1
    ZONE = 2


class CheckResults(Enum):
    OK = 0
    FAIL = 1
    CONTINUE = 2


@dataclass
class CurrentReturns:
    selected: int
    results_num: int
    failures_num: int
    cnd: Condition


@dataclass
class ClientStatus:
    status: str


@dataclass
class ServerReceivedSignal:
    status: Status


@dataclass
class ClientReceivedSignal:
    status: Status

