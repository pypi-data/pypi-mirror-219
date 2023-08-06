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
import vhcs.plan as plan
import vhcs.support.plan_util as util

@click.command()
@click.option("--file", "-f", type=click.File("rt"), required=False, help="Specified the combined plan file.")
@click.option("--resource", "-r", type=str, required=False, help="Specify a single resource in the plan to deploy. This includes deploying dependent resources.")
@click.option("--parallel/--sequential", type=bool, default=True, required=False, help="Specify deployment mode, parallel or sequential.")
def deploy(file, resource: str, parallel: bool):

    data, extra = util.load_plan(file)
    concurrency = 10 if parallel else 1

    try:        
        return plan.deploy(data, extra, resource, concurrency)
    except (FileNotFoundError, plan.PlanException) as e:
        return str(e), 1

# def _identify_files(file: list[str], name: str):
#     if not file and not name:
#         panic("Either --file or --name must be specified")
#     if file and name:
#         panic("--file and --name must not be specified together")
    
#     if name:
#         return [
#             name + '.blueprint.yml',
#             name + '.vars.yml',
#         ]
#     return file
