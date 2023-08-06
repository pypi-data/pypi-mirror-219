

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
from daisyfl.operator.base.client_logic import ClientLogic as BaseClientLogic
from daisyfl.client import Client
class ZoneClientLogic(BaseClientLogic):
    """Wrapper which adds SecAgg methods."""
    
    def __init__(self, client) -> None:
        self.client: Client = client
    