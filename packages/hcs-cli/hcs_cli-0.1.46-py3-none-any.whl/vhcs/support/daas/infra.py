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

from vhcs.common.ctxp import context


_config_name = "daas-infra"

def set(k: str, v: str):

    data = context.get(_config_name, default={})
    data = _with_default(data, _config_template)

    data[k] = v
    context.set(_config_name, data)

def unset(k: str):

    data = context.get(_config_name, default={})
    data = _with_default(data, _config_template)

    if k in data:
        del data[k]
        context.set(_config_name, data)

def get(k: str):
    return _get_config().get(k)

def all():
    return _get_config()

def save(data: dict):
    return context.set(_config_name, data)

def file():
    data = _get_config()
    context.set(_config_name, data)
    return context.file(_config_name)

def _get_config():
    data = context.get(_config_name, default={})
    return _with_default(data, _config_template)

def _with_default(target : dict, default : dict) -> dict:
    ret = dict(default)
    ret.update(target)
    return ret

_config_template = {
	"provider": {
		"id": "",
		"applicationId": "",
		"applicationSecret": ""
	},
	"network": {
		"vNetId": "",
		"tenantCIDRs": []
	},
	"desktop": {
		"markerId": "",
		"streamId": "",
		"templateType": "",
		"vmSkuName": ""
	}
}