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

from typing import Callable
from vhcs.plan import PlanException
import vhcs.service.admin as admin

def deploy(data: dict, save_state: Callable) -> dict:
    ret = admin.template.create(data)
    save_state(ret)
    id = ret['id']
    ready, template = admin.template.wait_for_template_ready(id, timeout_seconds=600)
    if not ready:
        save_state(template)
        raise PlanException("Template deployment failed.")
    return admin.template.get(id)

def refresh(data: dict, state: dict) -> dict:
    if state:
        id = state['id']
        if id:
            t = admin.template.get(id)
            if t:
                return t
    
    # Fall back with smart find by name
    name = data['name']
    search = 'name $eq ' + name
    templates = admin.template.list(org_id=data['orgId'], search=search)
    if templates:
        return templates[0]

def destroy(data: dict, state: dict) -> dict:
    if state:
        id = state['id']
        if id:
            admin.template.delete(id)
            admin.template.wait_for_template_deleted(id, 600)
            return
    
