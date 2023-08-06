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
"""Flower client app."""


from queue import Queue
from logging import INFO, ERROR, WARNING
from typing import Callable, Dict, Optional, Union, Tuple, List
import threading
import uuid

from daisyfl.common import (
    GRPC_MAX_MESSAGE_LENGTH,
    CURRENT_ROUND,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    CLIENT_OPERATOR,
    ZONE_CLIENT_OPERATOR,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
    IS_ZONE,
    CREDENTIAL,
    metadata_to_dict,
    dict_to_metadata,
    CID,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import (
    Code,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    GetParametersIns,
    GetParametersRes,
    GetPropertiesIns,
    GetPropertiesRes,
    NDArrays,
    Status,
    Report,
)

from .client import Client
from .client_api_handler import ClientListener
from .trainer import Trainer
from .grpc_client.connection import gRPCConnection
from .grpc_client.message_handler import set_client_operator_manager
from daisyfl.client.client_operator_manager import ClientOperatorManager
from .numpy_client import NumPyClient
from .numpy_client import has_evaluate as numpyclient_has_evaluate
from .numpy_client import has_fit as numpyclient_has_fit
from .numpy_client import has_get_parameters as numpyclient_has_get_parameters
from .numpy_client import has_get_properties as numpyclient_has_get_properties

EXCEPTION_MESSAGE_WRONG_RETURN_TYPE_FIT = """
NumPyClient.fit did not return a tuple with 3 elements.
The returned values should have the following type signature:

    Tuple[NDArrays, int, Dict[str, Scalar]]

Example
-------

    model.get_weights(), 10, {"accuracy": 0.95}

"""

EXCEPTION_MESSAGE_WRONG_RETURN_TYPE_EVALUATE = """
NumPyClient.evaluate did not return a tuple with 3 elements.
The returned values should have the following type signature:

    Tuple[float, int, Dict[str, Scalar]]

Example
-------

    0.5, 10, {"accuracy": 0.95}

"""


ClientLike = Union[Client, NumPyClient]


def start_client(
    *,
    parent_address: str,
    client: Client,
    grpc_max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
    root_certificates: Optional[bytes] = None,
    api_ip: str = None,
    api_port: int = None,
    metadata: Tuple = None,
    _zone: bool = False,
) -> None:
    # client_operator_manager
    client_operator_manager = ClientOperatorManager(client=client)
    operator_key = ZONE_CLIENT_OPERATOR if _zone else CLIENT_OPERATOR
    client_operator_manager.set_operator_key(key=operator_key)
    set_client_operator_manager(client_operator_manager)

    # check metadata
    if metadata is None:
        metadata = ()
    ## zone: process metadata
    if _zone:
        metadata_dict = metadata_to_dict(metadata=metadata, _check_required=False)
        metadata_dict[IS_ZONE] = "is_zone"
        if metadata_dict.__contains__(CREDENTIAL):
            log(WARNING, "CREDENTIAL is defined in the metadata of a zone. It will be ignored.")
            del metadata_dict[CREDENTIAL]
        if not metadata_dict.__contains__(CID):
            metadata_dict[CID] = str(uuid.uuid4())
        metadata = dict_to_metadata(metadata_dict)
    ## client: check metadata
    else:
        metadata_dict = metadata_to_dict(metadata=metadata)
        metadata = dict_to_metadata(metadata_dict)

    # declare instances: Trainer, gRPCConnection, ClientListener
    trainer = Trainer()
    connector = gRPCConnection(
        parent_address=parent_address,
        max_message_length=grpc_max_message_length,
        root_certificates=root_certificates,
        metadata=metadata,
        trainer=trainer,
    )
    listener = ClientListener(
        ip=api_ip,
        port=api_port,
        connector=connector,
        trainer=trainer,
    )
    trainer.set_connector(connector=connector)

    # start threads: ClientListener, gRPCConnection, Trainer
    
    ## ClientListener
    listener_thread = threading.Thread(target=listener.run, args=())
    listener_thread.setDaemon(True)
    listener_thread.start()
    ## gRPCConnection
    connector_thread = threading.Thread(target=connector.run, args=())
    connector_thread.setDaemon(True)
    connector_thread.start()
    ### check
    threading.Event().wait(timeout=1)
    if not listener_thread.is_alive():
        log(ERROR, "ClientListener failed")
        exit(1)
    if not connector_thread.is_alive():
        log(ERROR, "gRPCConnection failed")
        exit(1)
    ## Trainer
    trainer.run()


def start_numpy_client(
    *,
    parent_address: str,
    client: NumPyClient,
    grpc_max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
    root_certificates: Optional[bytes] = None,
    api_ip: str = None,
    api_port: int = None,
    metadata: Tuple = None,
    _zone: bool = False
) -> None:
    # Start
    start_client(
        parent_address=parent_address,
        client=_wrap_numpy_client(client=client),
        grpc_max_message_length=grpc_max_message_length,
        root_certificates=root_certificates,
        api_ip=api_ip,
        api_port=api_port,
        metadata=metadata,
        _zone=_zone,
    )
    if _zone:
        client.shutdown()


# wrap numpy_client to client
def to_client(client_like: ClientLike) -> Client:
    """Take any Client-like object and return it as a Client."""
    if isinstance(client_like, NumPyClient):
        return _wrap_numpy_client(client=client_like)
    return client_like


def _constructor(self: Client, numpy_client: NumPyClient) -> None:
    self.numpy_client = numpy_client  # type: ignore


def _get_properties(self: Client, ins: GetPropertiesIns) -> GetPropertiesRes:
    """Return the current client properties."""
    properties = self.numpy_client.get_properties(config=ins.config)  # type: ignore
    return GetPropertiesRes(
        status=Status(code=Code.OK, message="Success"),
        properties=properties,
    )


def _get_parameters(self: Client, ins: GetParametersIns) -> GetParametersRes:
    """Return the current local model parameters."""
    parameters = self.numpy_client.get_parameters(config=ins.config)  # type: ignore
    parameters_proto = ndarrays_to_parameters(parameters)
    return GetParametersRes(
        status=Status(code=Code.OK, message="Success"), parameters=parameters_proto
    )


def _fit(self: Client, ins: FitIns) -> FitRes:
    """Refine the provided parameters using the locally held dataset."""

    # Deconstruct FitIns
    parameters: NDArrays = parameters_to_ndarrays(ins.parameters)

    # Train
    results = self.numpy_client.fit(parameters, ins.config)  # type: ignore
    if not (
        len(results) == 3
        and isinstance(results[0], list)
        and isinstance(results[1], int)
        and isinstance(results[2], dict)
    ):
        raise Exception(EXCEPTION_MESSAGE_WRONG_RETURN_TYPE_FIT)
    # results -> Report.config
    parameters_prime, num_examples, config = results
    parameters_prime_proto = ndarrays_to_parameters(parameters_prime)
    if not config.__contains__(CURRENT_ROUND):
        config[CURRENT_ROUND] = ins.config[CURRENT_ROUND]
    if not config.__contains__(FIT_SAMPLES):
        config[FIT_SAMPLES] = num_examples
    if not config.__contains__(METRICS):
        config[METRICS] = {}
   
    # Return FitRes
    return FitRes(
        status=Status(code=Code.OK, message="Success"),
        parameters=parameters_prime_proto,
        config=config,
    )


def _evaluate(self: Client, ins: EvaluateIns) -> EvaluateRes:
    """Evaluate the provided parameters using the locally held dataset."""
    parameters: NDArrays = parameters_to_ndarrays(ins.parameters)

    results = self.numpy_client.evaluate(parameters, ins.config)  # type: ignore
    if not (
        len(results) == 3
        and isinstance(results[0], float)
        and isinstance(results[1], int)
        and isinstance(results[2], dict)
    ):
        raise Exception(EXCEPTION_MESSAGE_WRONG_RETURN_TYPE_EVALUATE)

    # results -> Report.config
    loss, num_examples, config = results
    if not config.__contains__(CURRENT_ROUND):
        config[CURRENT_ROUND] = ins.config[CURRENT_ROUND]
    if not config.__contains__(LOSS):
        config[LOSS] = loss
    if not config.__contains__(EVALUATE_SAMPLES):
        config[EVALUATE_SAMPLES] = num_examples
    if not config.__contains__(METRICS):
        config[METRICS] = {}
    
    # Return EvaluateRes
    return EvaluateRes(
        status=Status(code=Code.OK, message="Success"),
        config=config,
    )


def _wrap_numpy_client(client: NumPyClient) -> Client:
    member_dict: Dict[str, Callable] = {  # type: ignore
        "__init__": _constructor,
    }

    # Add wrapper type methods (if overridden)

    if numpyclient_has_get_properties(client=client):
        member_dict["get_properties"] = _get_properties

    if numpyclient_has_get_parameters(client=client):
        member_dict["get_parameters"] = _get_parameters

    if numpyclient_has_fit(client=client):
        member_dict["fit"] = _fit

    if numpyclient_has_evaluate(client=client):
        member_dict["evaluate"] = _evaluate

    # Create wrapper class
    wrapper_class = type("NumPyClientWrapper", (Client,), member_dict)

    # Create and return an instance of the newly created class
    return wrapper_class(numpy_client=client)  # type: ignore
