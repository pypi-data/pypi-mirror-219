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

import click
from vhcs.service import admin
from vhcs.common.ctxp import panic
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@option_org_id
@click.option("--label", "-l", type=str, required=False, default="AZURE")
@click.option("--name", "-n", type=str, required=True)
@click.option("--data", "-d", type=str, required=True, multiple=True, help="key-value separated by '='. This parameter can be specified multiple times.")
def create(org: str, label: str, name: str, data):
    """Create a provider instance."""
    data_obj = {}
    for d in data:
        k, v = d.split('=')
        data_obj[k] = v

    org_id = get_org_id(org)
    _validate(label, data_obj)

    payload = {
        "orgId": org_id,
        "providerLabel": label,
		"name": name,
		"edgeGatewayNeeded": True,
		"providerDetails": {
			"method": "ByAppRegistration",
			"data": data_obj
		}
	}
    ret = admin.provider.create(label, payload)
    if ret:
        return ret
    return "", 1

def _validate(label: str, data: dict):
    def _ensure_key_matches(required_keys, actual_keys):
        s1 = set(required_keys)
        s2 = set(actual_keys)
        missing = s1 - s2
        if missing:
            panic(f"Missing data: {missing}")
        extra = s2 - s1
        if extra:
            panic(f"Unexpected data: {extra}")

    label = label.upper()
    if label == 'AZURE':
        required_keys = ['subscriptionId', 'directoryId', 'applicationId', 'applicationKey', 'region']
        _ensure_key_matches(required_keys, data.keys())
    else:
        panic("Provider is not supported by CLI yet: " + label)
