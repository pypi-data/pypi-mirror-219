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
import vhcs.common.ctxp as ctxp
from vhcs.common.ctxp import panic, choose
from vhcs.plan.provider.azure import _az_facade as az
from vhcs.support.daas import infra
from vhcs.service import admin
from vhcs.support.daas import infra, helper, cidr_util

file_name = '.plan.yml'

@click.command()
@click.argument("name", type=str, required=True)
def plan(name: str):
    """Interactive setup for shared infrastructure."""

    def collect_information(data):
        vars = data['vars']
        _select_provider(vars['provider'])
        _input_azure_sp(vars['provider'])
        _select_vnet(vars['network'])
        _config_desktop_defaults(vars['desktop'])
        infra.save(data)

    return helper.prepare_plan_file(name, 'v1/infra.blueprint.yml', collect_information)
    

def _select_provider(data):
    providers = admin.provider.list(label='azure')
    if not providers:
        panic("No provider configured. Configure in HCS admin console first.")

    fn_provider_text = lambda p: f"{p['providerDetails']['data']['region']}, {p['name']}/{p['id']}"

    if len(providers) == 1:
        p = providers[0]
        click.echo("There's only one provider configured, and will be used: " + fn_provider_text(p))
    else:
        p = choose("Select region and provider", providers, fn_provider_text)
        if not p:
            return
    data['id'] = p['id']

def _input_azure_sp(data):
    data['applicationId'] = click.prompt("Input Azure service principle application ID", default=data['applicationId'] or "")
    data['applicationSecret'] = click.prompt("Input Azure service principle application secret", default=data['applicationSecret'] or "")

def _select_vnet(data):
    vnets = az.network.vnet.list()
    fn_get_text = lambda vnet: f"{vnet['name']} ({','.join(vnet['addressSpace']['addressPrefixes'])})"
    vnet = choose("Select vNet:", vnets, fn_get_text)
    data['vNetId'] = vnet['id']
    
    while True:
        tenant_cidrs = ctxp.util.input_array("Tenant CIDRs", default=data['tenantCIDRs'])
        if not tenant_cidrs:
            return
        err = _validate_cidr(tenant_cidrs, vnet['addressSpace']['addressPrefixes'])
        if err:
            click.echo(err)
        else:
            break
    data['tenantCIDRs'] = tenant_cidrs

def _validate_cidr(input, limit):
    is_subnet, problem = cidr_util.subnets_of(input, limit)
    if not is_subnet:
        return f"The specified CIDR {problem} is not subnet of vNet address spaces: {limit}"
    reserved_cidrs = [
        "172.17.0.0/26",    #docker bridge
		"192.170.0.0/21",   #podCidr
		"192.169.0.0/27",   #serviceCidr
    ]
    overlap, problem = cidr_util.overlaps(input, reserved_cidrs)
    if overlap:
        return f"The specified address {problem} conflict to reserved address spaces: {reserved_cidrs}"

def _config_desktop_defaults(data):
    groups = az.aad.group.list()
    fn_get_text = lambda g: g['displayName']
    prev = None
    for g in groups:
        if g['displayName'] == data['userGroup']:
            prev = g
    click.echo("To allow user login, they must have either 'Virtual Machine User Login' role or 'Virtual Machine Administrator Login' role.")
    selected = choose("Select a user group with one of the above roles:", groups, fn_get_text, selected=prev)
    data['userGroup'] = selected['displayName']
    