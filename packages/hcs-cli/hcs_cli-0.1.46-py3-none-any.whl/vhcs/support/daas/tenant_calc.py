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
from .cidr_util import find_available_cidr_24

log = logging.getLogger(__name__)

def deploy(data: dict) -> dict:
    provider = data['provider']
    provider_id = provider['id']
    log.info('Provider: %s', provider_id)
    providerInstance = admin.provider.get('azure', provider_id)
    if not providerInstance:
        raise PlanException('Provider not found: ' + provider_id)
    providerData = providerInstance['providerDetails']['data']
    subscription_id = providerData['subscriptionId']
    directory_id = providerData['directoryId']
    application_id = providerData['applicationId']
    region = providerData['region']
    log.info('Subscription: %s', subscription_id)
    log.info('Directory: %s', directory_id)
    log.info('ApplicationId: %s', application_id)
    log.info('Region: %s', region)

    template_type = data['desktop']['templateType']
    number_of_users = len(data['userEmails'])
    is_multi_session = "MULTI_SESSION" == template_type

    uag_deployments = admin.helper.list_resources_by_provider('uag-deployments', provider_id, limit=1)
    if not uag_deployments:
        raise Exception("No UAG deployment found.")
    uag_deployment_id = uag_deployments[0]['id']

    edge_deployments = admin.helper.list_resources_by_provider('edge-deployments', provider_id, limit=1)
    if not edge_deployments:
        raise Exception("No UAG deployment found.")
    edge_deployment_id = edge_deployments[0]['id']

    search = f"name $eq {data['desktop']['vmSkuName']}"
    vm_skus = admin.azure_infra.get_compute_vm_skus(provider_instance_id=provider_id, search=search, limit=1)
    if not vm_skus:
        raise Exception("No VM SKUs found.")

    template = {
        'total_vms': 1 if is_multi_session else number_of_users,
        'password': _generate_password(),
        'uag_deployment_id': uag_deployment_id,
        'edge_deployment_id': edge_deployment_id,
        'vm_sku': vm_skus[0]
    }

    org_idp_map = auth.admin.get_org_idp_map()
    cidr = _calculate_cidr(data)
    log.info('Calculated network address: %s', cidr)
    return {
        'location': region,
        'cidr': cidr,
        'vNet': az.network.vnet.get(data['network']['vNetId']),
        'providerInstance': providerInstance,
        'template': template,
        'number_of_users': number_of_users,
        'orgIdpMap': org_idp_map
    }

def _generate_password():
    from random import choice
    upper_chars = "ABCDEFGHJKLMNPQRSTUVWXY"
    readable_chars = "abcdefghjklmnpqrstuvwxy3456789"
    special_chars = "!@#$%_"
    return '' + choice(upper_chars) + ''.join(choice(readable_chars) for i in range(12)) + choice(special_chars)

def _calculate_cidr(data):
    network_cfg = data['network']

    vnet = az.network.vnet.get(network_cfg['vNetId'])
    vnet_cidrs = vnet['addressSpace']['addressPrefixes']
    used_cidrs = []
    for subnet in vnet['subnets']:
        used_cidrs.append(subnet['addressPrefix'])
    configured_cidrs = network_cfg['tenantCIDRs']

    tenant_cidr = find_available_cidr_24(vnet_cidrs, used_cidrs, configured_cidrs)
    if not tenant_cidr:
        raise PlanException("Unable to find usable subnet address space for the tenant. Consider adding new address space to the config via 'hcs daas infra plan', and/or add new spaces in vnet.")
    return tenant_cidr

def destroy(data: dict, prev: dict):
    return