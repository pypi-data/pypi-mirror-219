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
from .._util import hdc_service_client
from vhcs.util.query_util import with_query, PageRequest

_client = hdc_service_client("admin")

def get(id: str, **kwargs):
    url = with_query(f"/v2/templates/{id}", **kwargs)
    return _client.get(url)

def list(**kwargs):
    def _get_page(query_string):
        url = "/v2/templates?" + query_string
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()

def list_vms(template_id: str, **kwargs):
    def _get_page(query_string):
        url = f"/v2/templates/{template_id}/vms?" + query_string
        return _client.get(url)
    return PageRequest(_get_page, **kwargs).get()

def get_vm(template_id: str, vm_id: str, **kwargs):
    url = with_query(f"/v2/templates/{template_id}/vms/{vm_id}", **kwargs)
    return _client.get(url)

def create(payload):
    return _client.post("/v2/templates?ignore_warnings=true", json=payload)

def delete(id: str, force: bool = True):
    return _client.delete(f"/v2/templates/{id}?force={force}") 

def wait_for_template_deleted(id: str, timeout_seconds: int = 60):
    
    start = time.time()
    while True:
        t = get(id)
        if t == None:
            return True, None
        now = time.time()
        remaining_seconds = timeout_seconds - (now - start)
        if remaining_seconds < 1:
            return False, t
        sleep_seconds = remaining_seconds
        if sleep_seconds > 10:
            sleep_seconds = 10
        time.sleep(sleep_seconds)


def wait_for_template_ready(id: str, timeout_seconds: int = 60):
    start = time.time()
    while True:
        t = get(id)
        if t == None:
            return False, None
        status = t['reportedStatus'].get('statusValue')
        if status == 'READY':
            return True, t
        if status == 'ERROR':
            return False, t
        now = time.time()
        remaining_seconds = timeout_seconds - (now - start)
        if remaining_seconds < 1:
            return False, t
        sleep_seconds = remaining_seconds
        if sleep_seconds > 10:
            sleep_seconds = 10
        time.sleep(sleep_seconds)