from queue import Queue
from logging import INFO, DEBUG, ERROR
from daisyfl.common.logger import log
from typing import Callable, Dict, Optional, Union, Tuple, List
from threading import Lock, Event
from daisyfl.proto.transport_pb2 import ClientMessage, ServerMessage
from .grpc_client.message_handler import handle
from enum import Enum
from daisyfl.common import Status, Code, Parameters, serde

class TrainerStatus(Enum):
    RECEIVING = 1
    SENDING = 2
    CLOSE = 3

class Trainer:
    def __init__(
        self,
    ) -> None:
        self._status: TrainerStatus = TrainerStatus.RECEIVING
        self._lock_status: Lock = Lock()
        self._event_stop: Event = Event()
        self._shutdown: bool = False
        self._server_message: Optional[ServerMessage] = None
        self._client_message: Optional[ClientMessage] = None
    
    def run(self,) -> None:
        while not self._shutdown:
            # TODO: MTFL, while(receive) -> create a thread for handling and sending
            self._receiving()
            self._handling()
            self._sending()
        
    def _receiving(self,) -> None:
        while True:
            if self._status.value != 1:
                log(INFO, "Skip receiving")
                return None
            success = self._handle_connection(1)
            if not success:
                return None
            log(DEBUG, "Trainer tries receiving message")
            try:
                server_message, _ = self._connector.receive()
                self._connector.set_anchor(reset=False)
                with self._lock_status:
                    self._server_message = server_message
                    if self._status.value != 3:
                        self._status = TrainerStatus.SENDING
                    self._event_stop.clear()
                    ### === ###
                    """for loose association"""
                    self._connector.disconnect()
                    ### === ###
            except:
                log(DEBUG, "Reset Connection")
                self._connector.disconnect()
                self._connector.reconnect()
    
    def _handling(self,) -> None:
        if self._status.value != 2:
            log(INFO, "Skip handling")
            return None
        # TODO: Stop after Event.set()
        log(DEBUG, "Trainer tries handling ServerMessage")
        server_message: ServerMessage = self._server_message
        self._client_message = handle(server_message)
        self._server_message = None

    def _sending(self,) -> None:
        while True:
            if self._status.value != 2:
                log(INFO, "Skip sending")
                return None
            success = self._handle_connection(2)
            if not success:
                return None
            log(DEBUG, "Trainer tries sending message")
            try:
                client_message: ClientMessage = self._client_message
                self._connector.send(client_message)
                server_message, _ = self._connector.receive(timeout=3) # SRS
                self._connector.set_anchor(reset=True)
                with self._lock_status:
                    if self._status.value != 3:
                        self._client_message = None
                        self._status = TrainerStatus.RECEIVING
                    ### === ###
                    """for loose association"""
                    self._connector.disconnect()
                    ### === ###
                return None
            except:
                log(DEBUG, "Reset Connection")
                self._connector.disconnect()
                self._connector.reconnect()

    def _handle_connection(self, status_code: int) -> bool:
        while True:
            if self._status.value != status_code:
                return False
            event_dis = self._connector.event_disconn.is_set()
            event_rec = self._connector.event_reconn.is_set()
            if (not event_dis) and (not event_rec):
                # Connection Ready
                return True
            elif (event_dis) and (not event_rec):
                log(INFO, "Send reconnection request")
                self._connector.reconnect()
                Event().wait(timeout=1)
            elif (event_dis) and (event_rec):
                log(INFO, "Wait for reconnecting")
                Event().wait(timeout=1)
            else:
                log(ERROR, "Wait for reconnecting before disconnecting. It shouldn't happen.")

    # register functions
    def set_connector(
        self,
        connector,
    ) -> None:
        self._connector = connector

    # APIs
    def get_trainer_status_code(self,) -> int:
        return self._status.value

    def shutdown(self,) -> None:
        self._shutdown = True
        with self._lock_status:
            self._status = TrainerStatus.CLOSE
            # break from the current function
            self._connector.disconnect()
            self._event_stop.set()
        return
