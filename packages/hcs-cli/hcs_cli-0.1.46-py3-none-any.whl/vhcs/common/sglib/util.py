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
from vhcs.common.ctxp import CtxpException

option_org_id = click.option(
    "--org",
    type=str,
    default=None,
    required=False,
    help="Specify org ID. If not specified, org ID from the current auth token will be used.",
)

option_sort = click.option(
    "--sort",
    type=str,
    required=False,
    help="Ascending/Descending. Format is property,{asc|desc} and default is ascending",
)

option_limit = click.option(
    "--limit", 
    type=int, 
    required=False, 
    default=20, 
    help="Optionally, specify the number of records to fetch.")

def get_org_id(org: str) -> str:
    if org:
        return org

    from vhcs.common.sglib import auth

    auth_info = auth.details(False)
    if not auth_info:
        raise CtxpException("Not authorized. See 'hcs login --help'.")
    return auth_info.org.id
