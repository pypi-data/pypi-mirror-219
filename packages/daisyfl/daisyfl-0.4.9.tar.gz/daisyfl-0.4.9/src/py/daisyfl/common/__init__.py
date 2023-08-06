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
"""Flower utilities shared between server and client."""


from .parameter import bytes_to_ndarray as bytes_to_ndarray
from .parameter import ndarray_to_bytes as ndarray_to_bytes
from .parameter import ndarrays_to_parameters as ndarrays_to_parameters
from .parameter import parameters_to_ndarrays as parameters_to_ndarrays
from .parameter import encode_ndarrays as encode_ndarrays
from .parameter import decode_ndarrays as decode_ndarrays
from .metadata import metadata_to_dict as metadata_to_dict
from .metadata import dict_to_metadata as dict_to_metadata
from .metadata import ANCHOR as ANCHOR
from .metadata import HANDOVER as HANDOVER
from .metadata import IS_ZONE as IS_ZONE
from .metadata import CID as CID
from .metadata import CREDENTIAL as CREDENTIAL
from .metadata import DATASET as DATASET
from .metadata import DEVICE as DEVICE
from .metadata import ROOT_CERTIFICATES as ROOT_CERTIFICATES
from .typing import Code as Code
from .typing import DisconnectRes as DisconnectRes
from .typing import EvaluateIns as EvaluateIns
from .typing import EvaluateRes as EvaluateRes
from .typing import FitIns as FitIns
from .typing import FitRes as FitRes
from .typing import ClientStatus as ClientStatus
from .typing import ServerReceivedSignal as ServerReceivedSignal
from .typing import ClientReceivedSignal as ClientReceivedSignal
from .typing import GetParametersIns as GetParametersIns
from .typing import GetParametersRes as GetParametersRes
from .typing import GetPropertiesIns as GetPropertiesIns
from .typing import GetPropertiesRes as GetPropertiesRes
from .typing import Metrics as Metrics
from .typing import MetricsAggregationFn as MetricsAggregationFn
from .typing import NDArray as NDArray
from .typing import NDArrays as NDArrays
from .typing import Parameters as Parameters
from .typing import Properties as Properties
from .typing import ReconnectIns as ReconnectIns
from .typing import Scalar as Scalar
from .typing import Element as Element
from .typing import Status as Status
from .typing import Task as Task
from .typing import Report as Report
from .typing import Type as Type
from .typing import CheckResults as CheckResults
from .typing import CurrentReturns as CurrentReturns


GRPC_MAX_MESSAGE_LENGTH: int = 536_870_912  # == 512 * 1024 * 1024
NUM_ROUNDS = "NUM_ROUNDS"
CURRENT_ROUND = "CURRENT_ROUND"
EVALUATE = "EVALUATE"
TIMEOUT = "TIMEOUT"
FORWARDING_TIMEOUT = "FORWARDING_TIMEOUT"
FIT_SAMPLES = "FIT_SAMPLES"
EVALUATE_SAMPLES = "EVALUATE_SAMPLES"
LOSS = "LOSS"
METRICS = "METRICS"
ACCURACY = "ACCURACY"
TID = "TID"
SUBTASK = "SUBTASK"
EVALUATE_INTERVAL = "EVALUATE_INTERVAL"
MODEL_PATH = "MODEL_PATH"
REMOVE_OPERATOR = "REMOVE_OPERATOR"
OPERATORS = "OPERATORS"
MASTER_SERVER_OPERATOR = "MASTER_SERVER_OPERATOR"
CLIENT_OPERATOR = "CLIENT_OPERATOR"
ZONE_SERVER_OPERATOR = "ZONE_SERVER_OPERATOR"
ZONE_CLIENT_OPERATOR = "ZONE_CLIENT_OPERATOR"
STRATEGIES = "STRATEGIES"
MASTER_STRATEGY = "MASTER_STRATEGY"
ZONE_STRATEGY = "ZONE_STRATEGY"
PERIOD = "PERIOD"
CLIENT_HANDLING = "CLIENT_HANDLING"
CLIENT_IDLING = "CLIENT_IDLING"
SUBTASK_RETURNS_SELECTED = "SUBTASK_RETURNS_SELECTED"
SUBTASK_RETURNS_RESULTS = "SUBTASK_RETURNS_RESULTS"
SUBTASK_RETURNS_FAILURES = "SUBTASK_RETURNS_FAILURES"
SUBTASK_TIMER = "SUBTASK_TIMER"
TIMER_ROUND = "TIMER_ROUND"
INDIVIDUAL_CLIENT_METRICS = "INDIVIDUAL_CLIENT_METRICS"
PARTICIPATION = "PARTICIPATION"


__all__ = [
    "SUBTASK_RETURNS_SELECTED",
    "SUBTASK_RETURNS_RESULTS",
    "SUBTASK_RETURNS_FAILURES",
    "PARTICIPATION",
    "SUBTASK_TIMER",
    "TIMER_ROUND",
    "INDIVIDUAL_CLIENT_METRICS",
    "NUM_ROUNDS",
    "CURRENT_ROUND",
    "EVALUATE",
    "TIMEOUT",
    "FORWARDING_TIMEOUT",
    "SUBTASK",
    "FIT_SAMPLES",
    "EVALUATE_SAMPLES",
    "LOSS",
    "METRICS",
    "ACCURACY",
    "EVALUATE_INTERVAL",
    "MODEL_PATH",
    "Type",
    "CheckResults",
    "CurrentReturns",
    "encode_ndarrays",
    "decode_ndarrays",
    "bytes_to_ndarray",
    "metadata_to_dict",
    "dict_to_metadata",
    "Code",
    "Element",
    "DisconnectRes",
    "EvaluateIns",
    "EvaluateRes",
    "FitIns",
    "FitRes",
    "GetParametersIns",
    "GetParametersRes",
    "GetPropertiesIns",
    "GetPropertiesRes",
    "ClientStatus",
    "ServerReceivedSignal",
    "ClientReceivedSignal",
    "GRPC_MAX_MESSAGE_LENGTH",
    "Metrics",
    "MetricsAggregationFn",
    "ndarray_to_bytes",
    "NDArray",
    "NDArrays",
    "ndarrays_to_parameters",
    "Parameters",
    "parameters_to_ndarrays",
    "Properties",
    "ReconnectIns",
    "Scalar",
    "Status",
    "Task",
    "Report",
    "TID",
    "REMOVE_OPERATOR",
    "OPERATORS",
    "MASTER_SERVER_OPERATOR",
    "CLIENT_OPERATOR",
    "ZONE_SERVER_OPERATOR",
    "ZONE_CLIENT_OPERATOR",
    "STRATEGIES",
    "MASTER_STRATEGY",
    "ZONE_STRATEGY",
    "PERIOD",
    "CREDENTIAL",
    "IS_ZONE",
    "CLIENT_HANDLING",
    "CLIENT_IDLING",
    "ANCHOR",
    "ROOT_CERTIFICATES",
    "HANDOVER",
    "CID",
    "DATASET",
    "DEVICE",
]
