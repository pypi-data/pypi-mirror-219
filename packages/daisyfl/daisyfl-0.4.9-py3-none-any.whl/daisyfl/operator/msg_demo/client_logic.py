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
from daisyfl.common import (
    Status,
    Code,
    FitIns,
    FitRes,
    EvaluateIns,
    EvaluateRes,
)
from daisyfl.common.logger import log
from logging import DEBUG, ERROR, INFO, WARNING
from .msg import (
    WHO_CREATE_THIS_DEMO,
    TIME,
    STUDENT,
    Time,
    Student,
)
from daisyfl.operator.base.client_logic import ClientLogic as BaseClientLogic
from daisyfl.client import Client

class ClientLogic(BaseClientLogic):
    """Wrapper which adds SecAgg methods."""
    
    def __init__(self, client: Client) -> None:
        self.client: Client = client
    
    def fit(
        self, ins: FitIns,
    ) -> FitRes:
        stage = Time(ins.config[TIME])
        if stage == Time.SAY_HI:
            return _say_hi(ins)
        elif stage == Time.TRAIN:
            return _fit(self, ins)
        else:
            raise ValueError("Invalid stage received")


def _say_hi(ins: FitIns) -> FitRes:
    log(INFO,
        "\nHello, %s.\nI am %s.\nNice to meet you.",
        ins.config[WHO_CREATE_THIS_DEMO],
        ins.config[STUDENT]["name"],
    )
    return FitRes(
        status=Status(code=Code.OK, message="Success"),
        parameters=ins.parameters,
        config=ins.config,
    )

def _fit(client_logic: ClientLogic, ins: FitIns) -> FitRes:
    return client_logic.client.fit(ins)