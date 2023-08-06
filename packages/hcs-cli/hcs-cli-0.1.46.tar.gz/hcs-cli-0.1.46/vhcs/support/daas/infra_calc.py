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
import logging
from vhcs.service import admin, auth
from vhcs.plan.provider.azure import _az_facade as az
from vhcs.plan import PlanException

log = logging.getLogger(__name__)

def deploy(data: dict, save_state) -> dict:
    provider = data['provider']
    provider_id = provider['id']
    log.info('Provider: %s', provider_id)
    providerInstance = admin.provider.get('azure', provider_id)
    if not providerInstance:
        raise PlanException('Provider not found: ' + provider_id)
    providerData = providerInstance['providerDetails']['data']
    region = providerData['region']
    return {
        'location': region
    }

def destroy(data: dict, prev: dict):
    return