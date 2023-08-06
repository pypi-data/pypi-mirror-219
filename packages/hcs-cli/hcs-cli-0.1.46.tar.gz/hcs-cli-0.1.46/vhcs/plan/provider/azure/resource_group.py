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

from . import _az_facade as az

def deploy(data: dict) -> dict:
    name = data['name']
    location = data['location']
    tags = data.get('tags')
    return az.resource_group.create(name, location, tags)

def refresh(data: dict, state: dict) -> dict:
    return state

def destroy(data: dict, state: dict) -> dict:
    name = data['name']
    return az.resource_group.delete(name)