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
"""Flower client (abstract base class)."""


from abc import ABC, abstractmethod
from typing import Optional, Union, Callable

from daisyfl.common import (
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    GetParametersIns,
    GetParametersRes,
    GetPropertiesIns,
    GetPropertiesRes,
    Properties,
    ReconnectIns,
)
from daisyfl.proto.transport_pb2 import ClientMessage


class ClientProxy(ABC):
    """Abstract base class for Flower client proxies."""

    def __init__(self, cid: str):
        self.cid = cid
        self.properties: Properties = {}

    @abstractmethod
    def get_properties(
        self,
        ins: GetPropertiesIns,
    ) -> None:
        """Returns the client's properties."""

    @abstractmethod
    def get_parameters(
        self,
        ins: GetParametersIns,
    ) -> None:
        """Return the current local model parameters."""

    @abstractmethod
    def fit(
        self,
        ins: FitIns,
    ) -> None:
        """Refine the provided parameters using the locally held dataset."""

    @abstractmethod
    def evaluate(
        self,
        ins: EvaluateIns,
    ) -> None:
        """Evaluate the provided parameters using the locally held dataset."""

    @abstractmethod
    def reconnect(
        self,
        ins: ReconnectIns,
    ) -> None:
        """Disconnect and (optionally) reconnect later."""
    
    @abstractmethod
    def submit_client_message(
        self,
        client_message: ClientMessage,
    ) -> None:
        """Receive, deserialize, and submit"""

    @abstractmethod
    def set_submit_subtask_fn(self, submit_subtask: Callable) -> None:
        """Set callback function"""
