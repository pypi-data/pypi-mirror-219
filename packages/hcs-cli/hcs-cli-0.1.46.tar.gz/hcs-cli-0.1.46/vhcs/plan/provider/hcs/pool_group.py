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

import vhcs.service.portal as portal

def deploy(data: dict) -> dict:
    return portal.pool.create(data)

def refresh(data: dict, state: dict) -> dict:
    if state:
        id = state.get('id')
        if id:
            return portal.pool.get(id, data['orgId'])
    
    # Fall back with smart find by name
    pools = portal.pool.list(search=f"name $eq {data['name']}")
    if pools and len(pools) == 1:
        return pools[0]
    return state

def destroy(data: dict, state: dict) -> dict:
    if state:
        id = state.get('id')
        if id:
            return portal.pool.delete(id, data['orgId'])
    return state