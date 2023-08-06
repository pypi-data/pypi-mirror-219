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

from vhcs.service import admin

def deploy(data: dict) -> dict:
    return admin.provider.create(data)

def refresh(data: dict, state: dict) -> dict:
    org_id = data['orgId']
    label = data['label']
    if state:
        id = state.get('id')
        if id:
            return admin.provider.get(label, id)
    
    # Fall back with smart find by name
    return admin.provider.find_by_name(data['name'], org_id)

def destroy(data: dict, state: dict) -> dict:
    org_id = data['orgId']
    label = data['label']
    id = state['id']
    return admin.provider.delete(label, id, org_id)