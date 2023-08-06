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

from .._util import hdc_service_client
from vhcs.util.query_util import with_query, PageRequest

_client = hdc_service_client("admin")

def list(**kwargs):
    def _get_page(query_string):
        url = "/v2/templates?" + query_string
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()

def list_resources_by_provider(resource_type: str, provider_instance_id: str, limit: int = 10):
    def _get_page(query_string):
        url = f"/v2/{resource_type}?" + query_string
        return _client.get(url)

    search = f"providerInstanceId $eq {provider_instance_id}"
    return PageRequest(_get_page, search=search, limit=limit).get()

