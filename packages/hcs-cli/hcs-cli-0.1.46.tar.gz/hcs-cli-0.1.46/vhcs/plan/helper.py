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

import json
import yaml
from typing import Tuple
import os
from vhcs.common.util import load_data_file, strict_dict_to_class, process_variables

class PlanException(Exception):
    pass

class Blueprint:
    vars: dict
    defaults: dict = {}
    providers: list = []
    resources: list

    def __repr__(self):
        return f"Blueprint"

def load_files(files: list[str]) -> dict:
    ret = {}
    for file in files:
        data = load_data_file(file)
        if data == None or isinstance(data, str):
            raise FileNotFoundError("Fail loading file: " + file)
        ret = _merge_dict_fail_on_dup(ret, _smart_load_file(file))
    return ret


def process_template(template) -> Tuple[dict, dict]:
    bp, pending = _materialize_blueprint(template)
    _validate_blueprint(bp)
    return bp, pending

def _validate_blueprint(blueprint: dict):
    _validate_resource_id_no_dup(blueprint)
    _validate_resource_id_not_conflict_to_reserved_names(blueprint)
    _validate_resource_id_not_conflict_to_provider_types(blueprint)
    _validate_no_duplicate_provider_config(blueprint)
    _validate_statement_after(blueprint)

def _get_duplicates(lst):
    return [item for item in set(lst) if lst.count(item) > 1]

def _validate_statement_after(blueprint: dict):

    def _raise(owner, reason):
        raise PlanException(f"Invalid statement: after. Owner={owner}, reason={reason}.")
    
    def _validate_after(target_name, owner_resource_name):
        if not isinstance(target_name, str):
            _raise(owner_resource_name, f"Invalid value type: {type(target_name).__name__}")
    
        if target_name not in blueprint['resources']:
            _raise(owner_resource_name, "Target not found: " + target_name)

    for k, v in blueprint['resources'].items():
        after = v.get('after')
        if after:
            if isinstance(after, list):
                for a in after:
                    _validate_after(a, k)

                dup = _get_duplicates(after)
                if dup:
                    _raise(k, 'Duplicated keys: ' + dup)
            elif isinstance(after, str):
                _validate_after(after, k)
            else:
                _raise(k, "Invalid type, expect str or list, got: " + type(after).__name__)

def _validate_no_duplicate_provider_config(blueprint: dict):
    providers = blueprint.get('providers')
    if not providers:
        return
    known_types = []
    for r in providers:
        t = r['type']
        if t in known_types:
            raise PlanException("Invalid blueprint. Duplicated provider config: " + r['type'])
        known_types.append(t)

def _validate_resource_id_not_conflict_to_provider_types(blueprint: dict):
    provider_names = set()
    for k, v in blueprint['resources'].items():
        name, _ = v['kind'].split('/')
        provider_names.add(name)
    for name in blueprint['resources']:
        if name in provider_names:
            raise PlanException("Invalid blueprint. Invalid resource name due to conflict to provider type. Name: " + name)
        
def _validate_resource_id_no_dup(blueprint: dict):
    resource_names = set()
    for name in blueprint['resources']:
        if name in resource_names:
            raise PlanException("Invalid blueprint. Duplicated resource name: " + name)
        resource_names.add(name)

def _validate_resource_id_not_conflict_to_reserved_names(blueprint: dict):
    reserved_names_for_state = ['result', 'pending', 'log', 'destroy_output']
    reserved_names_for_blueprint = ['defaults', 'vars', 'providers', 'resources']
    reserved_names_for_function = ['profile', 'context']
    existing_names_top_level = blueprint.keys()
    reserved_names = set([*existing_names_top_level, *reserved_names_for_blueprint, *reserved_names_for_state, *reserved_names_for_function])
    for name in blueprint['resources']:
        if name in reserved_names:
            raise PlanException("Invalid blueprint. Resource name conflicts to a reserved name: " + name)

def _smart_load_file(file: str):
    if not os.path.exists(file):
        raise Exception("File not found: " + file)
    if not os.path.isfile(file):
        raise Exception("Not a file: " + file)
    if file.endswith('.json'):
        with open(file, "r") as f:
            return json.load(f)
    elif file.endswith('.yaml') or file.endswith('.yml'):
        with open(file, "r") as f:
            return yaml.safe_load(f)
    else:
        raise Exception("Unknown file extention: " + file)
    
def _merge_dict_fail_on_dup(o1: dict, o2: dict) -> dict:
    ret = dict(o1)
    for k, v in o2.items():
        if k in o1:
            raise Exception("Fail processing file. Duplicated key found: " + k)
        ret[k] = v
    return ret


def _materialize_blueprint(template: dict) -> Tuple[dict, dict]:
    ret = process_variables(template)
    return template, ret['pending']
