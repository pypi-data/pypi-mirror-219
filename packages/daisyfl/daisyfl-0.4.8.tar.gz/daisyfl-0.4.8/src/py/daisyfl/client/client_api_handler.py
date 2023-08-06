from flask import Flask, request
from typing import Callable
from logging import INFO
from daisyfl.common.logger import log

class ClientListener:
    def __init__(
            self,
            ip: str,
            port: int,
            trainer,
            connector,
        ):
        self.app = Flask(__name__)
        self._ip: str = ip
        self._port: int = port
        self._connector = connector
        self._trainer = trainer
        
        @self.app.route("/reconnect", methods=["POST"])
        def reconnect():
            self._connector.reconnect()
            return {}, 200

        @self.app.route("/shutdown", methods=["POST"])
        def shutdown():
            self._trainer.shutdown()
            return {}, 200
        
        @self.app.route("/handover", methods=["POST"])
        def handover():
            js = request.get_json()
            if not js.__contains__("address"):
                log(INFO, "Please define the new parent address with the value of the key \"address\"")
                js["address"] = None
            self._connector.handover(js["address"])
            return js, 200

        @self.app.route("/disconnect", methods=["POST"])
        def disconnect():
            self._connector.disconnect()
            return {}, 200


    def run(self,):
        self.app.run(host=self._ip, port=self._port)

