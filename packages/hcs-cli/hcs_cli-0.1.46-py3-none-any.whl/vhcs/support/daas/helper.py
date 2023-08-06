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
import yaml
from typing import Callable
from vhcs.plan.provider.azure import _az_facade as az
from vhcs.service import admin
from . import template, infra
from vhcs.common import util as data_util
from vhcs.plan import PlanException

log = logging.getLogger(__file__)

def prep_az_cli(tenant_request):
    provider = tenant_request['provider']
    providerInstanceId = provider['providerInstanceId']
    print('Provider:', providerInstanceId)
    providerInstance = admin.provider.get('azure', providerInstanceId)
    subscription_id = providerInstance['providerDetails']['data']['subscriptionId']
    directory_id = providerInstance['providerDetails']['data']['directoryId']
    application_id = providerInstance['providerDetails']['data']['applicationId']
    region = providerInstance['providerDetails']['data']['region']
    print('Subscription:', subscription_id)
    print('Directory:', directory_id)
    print('ApplicationId:', application_id)
    print('Region:', region)
    if application_id != provider['applicationId']:
        log.warning("Configured application ID for CLI does not match application ID for provider.")
    
    az.login(provider['applicationId'], provider['applicationSecret'], directory_id)
    az.set_subscription(subscription_id)

def prepare_plan_file(deployment_id: str, blueprint_id: str, fn_collect_info: Callable):
    suffix = '.blueprint.yml'

    if blueprint_id.endswith(suffix):
        blueprint_id = blueprint_id[:-len(suffix)]

    input_data = template.get(blueprint_id + '.vars.yml')
    file_name = _get_file_name(deployment_id)

    # Apply previous input, if any
    prev = data_util.load_data_file(file_name)
    if prev:
        prev_vars = prev.get('vars')
        if prev_vars:
            data_util.deep_apply_defaults(input_data['vars'], prev_vars)

    # Add defaults from shared infra config, if anything missing
    data_util.deep_apply_defaults(input_data, infra.all())
    
    # Enforce key values
    input_data['deploymentId'] = deployment_id
    input_data['vars']['orgId'] = _get_org_id()
    
    # Collect input from user
    fn_collect_info(input_data)

    # Combine and save
    blueprint_file = blueprint_id + '.blueprint.yml'
    blueprint = template.get(blueprint_file)
    text = "\n".join([
        yaml.safe_dump(input_data, sort_keys=False),
        "",
        "# ----------------------------------",
        "# Blueprint: " + blueprint_file,
        "",
        yaml.safe_dump(blueprint, sort_keys=False)
    ])

    with open(file_name, "w") as file:
        file.write(text)

    print("Plan saved as file: " + file_name)
    print(f"To view the plan:   'hcs plan graph -f {file_name}'")
    print(f"To deploy the plan: 'hcs plan deploy -f {file_name}'")

def _get_file_name(deployment_id: str) -> str:
    return deployment_id + '.plan.yml'

def _get_org_id():
    from vhcs.common.sglib import auth
    auth_info = auth.details(get_org_details=False)
    return auth_info.org.id
