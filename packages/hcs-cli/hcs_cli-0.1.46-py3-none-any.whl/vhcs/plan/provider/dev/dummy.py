"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import time
from copy import deepcopy
from typing import Callable
import vhcs.common.duration as duration
from vhcs.plan import PlanException

def deploy(data: dict, save_state: Callable) -> dict:

    text = data.get('text')
    error = data.get('error')
    delay = data.get('delay')
    error_before_save = data.get('error_before_save')

    delay_seconds = duration.to_seconds(delay)
    if delay_seconds:
        time.sleep(delay_seconds)
    ret = deepcopy(data)
    ret['outputText'] = text

    if not error_before_save:
        save_state(ret)

    if error:
        raise PlanException(error)
        
    return ret

def refresh(data: dict, state: dict) -> dict:
    return state

def destroy(data: dict, state: dict) -> dict:
    return {}