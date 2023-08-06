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

from ulid import ULID
import vhcs.common.ctxp as ctxp

def _store() -> ctxp.fstore:
    return ctxp.profile_store('daas-tenant')

_config_template = {
    "id": "",
    "customerName": "",
    "applicationId": "",
    "applicationSecret": "",
    "desktopName": "",
    "groupName": "",
    "markerId": "",
    "orgId": "",
    "providerInstanceId": "",
    "streamId": "",
    "templateType": "",
    "userEmails": "",
    "vmSkuName": ""
}

def _with_default(target : dict, default : dict) -> dict:
    ret = dict(default)
    if target:
        ret.update(target)
    return ret

def list():
    return _store().values()

def names():
    ret = []
    for v in list():
        ret.append(v['customerName'])
    return ret

def ids():
    return _store().keys()

def get(id: str):
    return _store().get(id)

def find_by_customer_name(customer_name: str):
    for doc in list():
        if doc['customerName'] == customer_name:
            return doc

def save(id: str, data: dict):
    return _store().save(id, data)

def delete(id: str):
    return _store().delete(id)

def create(customer_name: str):
    data = find_by_customer_name(customer_name)
    if data:
        raise ctxp.CtxpException("A tenant with that name already exists.")
    data = _with_default(data, _config_template)
    data['id'] = str(ULID())
    data['customerName'] = customer_name
    return data
