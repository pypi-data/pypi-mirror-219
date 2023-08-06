# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in trainerliance with the License.
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
"""Contextmanager managing a gRPC channel to the Flower server."""


from contextlib import contextmanager
from logging import DEBUG, INFO, WARNING, ERROR
from queue import Queue
from typing import Callable, Iterator, Optional, Tuple, Any, Dict, List

import grpc
from threading import Condition, Event, Lock

from daisyfl.common import (
    HANDOVER,
    ROOT_CERTIFICATES,
    ANCHOR,
    GRPC_MAX_MESSAGE_LENGTH,
    CLIENT_IDLING,
    CLIENT_HANDLING,
    serde,
    ClientStatus,
    metadata_to_dict,
    dict_to_metadata,
)
from daisyfl.common.logger import log
from daisyfl.proto.transport_pb2 import ClientMessage, ServerMessage
from daisyfl.proto.transport_pb2_grpc import FlowerServiceStub
from iterators import TimeoutIterator

# The following flags can be uncommented for debugging. Other possible values:
# https://github.com/grpc/grpc/blob/master/doc/environment_variables.md
# import os
# os.environ["GRPC_VERBOSITY"] = "debug"
# os.environ["GRPC_TRACE"] = "tcp,http"

def process_metadata(
    metadata: Tuple,
    anchor: Optional[str],
    root_certificates: Optional[bytes],
    handover: bool,
) -> Tuple:
    metadata_dict = metadata_to_dict(metadata, _check_reserved = False)
    
    if anchor is not None:
        metadata_dict[ANCHOR] = anchor
    elif metadata_dict.__contains__(ANCHOR):
        del metadata_dict[ANCHOR]
    
    if root_certificates is not None:
        metadata_dict[ROOT_CERTIFICATES] = root_certificates
    elif metadata_dict.__contains__(ROOT_CERTIFICATES):
        del metadata_dict[ROOT_CERTIFICATES]
    
    if handover:
        metadata_dict[HANDOVER] = "handover"
    elif metadata_dict.__contains__(HANDOVER):
        del metadata_dict[HANDOVER]
    
    return dict_to_metadata(metadata_dict)

def on_channel_state_change(channel_connectivity: str) -> None:
    """Log channel connectivity."""
    log(DEBUG, channel_connectivity)

class gRPCConnection:
    def __init__(self,
        # for grpc_connection
        parent_address: str = None,
        max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
        root_certificates: Optional[bytes] = None,
        metadata: Tuple = (),
        # sync up
        trainer = None,
    ):
        self.queue: Queue[ClientMessage] = None
        # channel
        self._close_channel: Callable = None
        self._on_channel_state_change: Callable = on_channel_state_change
        # transmission
        self.send: Callable = None
        self.receive: Callable = None
        # for grpc_connection
        self._parent_address: str = parent_address
        self._max_message_length: int = max_message_length
        self._root_certificates: Optional[bytes] = root_certificates
        self._metadata: Tuple = metadata
        self._anchor: str = None
        self.sleep_duration: int = 2
        # conditions
        self.event_disconn: Event = Event()
        self.event_disconn.set()
        self.event_reconn: Event = Event()
        self._cnd_api: Condition = Condition()
        self._busy: bool = False
        # sync up
        self._trainer = trainer
        
    def run(self,):
        while True:
            # Wait for Trainer ready and for reconnection
            log(DEBUG, "Connector idling")
            self.event_reconn.wait()
            log(DEBUG, "Connector reconnecting")
            try:
                with self.grpc_connection() as conn:
                    send, receive = conn
                    self.receive = receive
                    self.send = send
                    # send ClientStatus
                    status_code = self._trainer.get_trainer_status_code()
                    if status_code == 1:
                        client_status = serde.client_status_to_proto(ClientStatus(status=CLIENT_IDLING))
                    elif status_code == 2:
                        client_status = serde.client_status_to_proto(ClientStatus(status=CLIENT_HANDLING))
                    else:
                        log(ERROR, "Trainer should be closed.")
                    client_message = ClientMessage(client_status=client_status)
                    send(client_message)
                    # Trainer can use
                    self.event_reconn.clear()
                    self.event_disconn.clear()
                    log(DEBUG, "Trainer's term")
                    log(INFO, "Sleep for " + str(self.sleep_duration) + " seconds")
                    # Wait for ConnectionFail
                    self.event_disconn.wait()
                    log(DEBUG, "Connector's term")
                    Event().wait(timeout=self.sleep_duration)
            except:
                log(INFO, "Sleep for " + str(self.sleep_duration) + " seconds")
                Event().wait(timeout=self.sleep_duration)
    
    @contextmanager
    def grpc_connection(
        self,
    ) -> Iterator[Tuple[Callable[[], ServerMessage], Callable[[ClientMessage], None]]]:
        # Possible options:
        # https://github.com/grpc/grpc/blob/v1.43.x/include/grpc/impl/codegen/grpc_types.h
        channel_options = [
            ("grpc.max_send_message_length", self._max_message_length),
            ("grpc.max_receive_message_length", self._max_message_length),
        ]

        if self._root_certificates is not None:
            ssl_channel_credentials = grpc.ssl_channel_credentials(self._root_certificates)
            channel = grpc.secure_channel(
                self._parent_address, ssl_channel_credentials, options=channel_options
            )
            log(INFO, "Opened secure gRPC connection using certificates")
        else:
            channel = grpc.insecure_channel(self._parent_address, options=channel_options)
            log(INFO, "Opened insecure gRPC connection (no certificates were passed)")

        channel.subscribe(on_channel_state_change)
        self._close_channel = channel.close

        
        stub = FlowerServiceStub(channel)
        self.queue: Queue[ClientMessage] = Queue(maxsize=1)
        self._metadata = process_metadata(metadata=self._metadata, anchor=self._anchor, root_certificates=self._root_certificates, handover=self.check_handover())
        server_message_iterator: Iterator[ServerMessage] = stub.Join(iter(self.queue.get, None), metadata=self._metadata)

        def receive_fn(timeout: Optional[int] = None) -> Tuple[ServerMessage, bool]:
            timeout_iterator = TimeoutIterator(iterator=server_message_iterator, reset_on_next=True)
            if timeout is not None:
                timeout_iterator.set_timeout(float(timeout))
            server_message = next(timeout_iterator)
            if server_message is timeout_iterator.get_sentinel():
                return server_message, False
            return server_message, True
        receive: Callable[[Optional[int]], Tuple[ServerMessage, bool]] = receive_fn
        send: Callable[[ClientMessage], None] = lambda msg: self.queue.put(msg, block=False)

        try:
            yield send, receive
        finally:
            # Make sure to have a final
            channel.close()
            log(DEBUG, "gRPC channel closed")

    def set_anchor(self, reset: bool = True) -> None:
        if reset:
            self._anchor = None
        else:    
            self._anchor = self._parent_address

    def check_handover(self, ) -> bool:
        if (self._anchor is not None) and (self._parent_address is not None):
            if self._anchor != self._parent_address:
                return True
        return False


    # external APIs
    def reconnect(self,) -> bool:
        with self._cnd_api:
            while self._busy:
                self._cnd_api.wait()
            self._busy = True
        ###
        result = False
        if not self.event_disconn.is_set():
            log(
                WARNING,
                "Try reconnecting before disconnecting. " + \
                "Do nothing."
            )
        elif self.event_reconn.is_set():
            log(
                WARNING,
                "Another reconnection request has not been handled or the connection has not been built. " + \
                "Do nothing."
            )
        else:
            self.event_reconn.set()
            result = True
        ###
        self._busy = False
        with self._cnd_api:
            self._cnd_api.notify_all()
        return result

    def disconnect(self,) -> bool:
        with self._cnd_api:
            while self._busy:
                self._cnd_api.wait()
            self._busy = True
        ###
        result = False
        if self.event_disconn.is_set():
            log(
                WARNING,
                "Another disconnection request has not been handled or the connection has not been built. " + \
                "Do nothing."
            )
        else:
            self.event_disconn.set()
            result = True
        ###
        self._busy = False
        with self._cnd_api:
            self._cnd_api.notify_all()
        return result

    def handover(self, new_parent_address: str) -> None:
        with self._cnd_api:
            while self._busy:
                self._cnd_api.wait()
            self._busy = True
        ###
        if new_parent_address is not None:
            self._parent_address = new_parent_address
        ###
        self._busy = False
        with self._cnd_api:
            self._cnd_api.notify_all()
