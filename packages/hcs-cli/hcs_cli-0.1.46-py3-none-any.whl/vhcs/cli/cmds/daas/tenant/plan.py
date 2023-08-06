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
from vhcs.service import admin, ims_catalog
from vhcs.common.ctxp import choose, util as cli_util
from vhcs.support.daas import infra, helper


@click.command()
@click.argument("name", type=str, required=True)
def plan(name: str):
    """Interactive command to request a DaaS tenant"""
    return helper.prepare_plan_file(name, 'v1/tenant.blueprint.yml', _collect_info)

def _collect_info(data):
    #_fill_info_from_infra()
    vars = data['vars']
    _config_desktop(vars)
    _input_user_emails(vars)

def _config_desktop(data):

    def _select_image_and_vm_sku(data):
        images = ims_catalog.helper.get_images_by_provider_instance_with_asset_details(data['provider']['id'])
        fn_get_text = lambda d: f"{d['name']}: {d['description']}"
        prev_selected_image = None
        if data['desktop']['streamId']:
            for i in images:
                if i['id'] == data['desktop']['streamId']:
                    prev_selected_image = i
                    break
        selected_image = choose("Select image:", images, fn_get_text, selected=prev_selected_image)
        data['desktop']['streamId'] = selected_image['id']

        fn_get_text = lambda m: f"{m['name']}"
        selected_marker = choose("Select marker:", selected_image['markers'], fn_get_text)
        data['desktop']['markerId'] = selected_marker['id']

        image_asset_details = selected_image['_assetDetails']['data']

        search = f"capabilities.HyperVGenerations $in {image_asset_details['generationType']}"
        vm_skus = admin.azure_infra.get_compute_vm_skus(data['provider']['id'], limit=200, search=search)
        prev_selected_vm_sku = None
        if data['desktop']['vmSkuName']:
            selected_vm_sku_name = data['desktop']['vmSkuName']
        else:
            selected_vm_sku_name = image_asset_details['vmSize']
        if selected_vm_sku_name:
            for sku in vm_skus:
                if sku['id'] == selected_vm_sku_name:
                    prev_selected_vm_sku = sku
                    break

        fn_get_text = lambda d: f"{d['data']['name']} (CPU: {d['data']['capabilities']['vCPUs']}, RAM: {d['data']['capabilities']['MemoryGB']})"

        selected = choose("Select VM size:", vm_skus, fn_get_text, selected=prev_selected_vm_sku)
        data['desktop']['vmSkuName'] = selected['data']['name']

    def _select_desktop_type(data):
        types = ['MULTI_SESSION', 'FLOATING']
        data['desktop']['templateType'] = choose("Desktop type:", types)

    _select_image_and_vm_sku(data)
    _select_desktop_type(data)

def _input_user_emails(data):
    data['userEmails'] = cli_util.input_array("User emails", default=data['userEmails'])
