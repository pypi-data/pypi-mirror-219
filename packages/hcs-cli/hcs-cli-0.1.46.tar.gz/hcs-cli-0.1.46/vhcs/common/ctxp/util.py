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

import os
import subprocess
import json
import yaml
import types
import sys
import httpx
import traceback
import click
from typing import Any, Callable
import questionary


class CtxpException(Exception):
    pass

def error(reason: any, return_code: int = 1) -> tuple[CtxpException, int]:
    
    # Shortcut if the reason is an Exception already
    if isinstance(reason, Exception):
        return reason, return_code
    
    # Convert reason to string and wrap as CtxpException
    if isinstance(reason, str):
        pass
    elif isinstance(reason, dict):
        reason = json.dumps(reason, indent=4)
    else:
        reason = str(reason)
    return CtxpException(reason), return_code

def validate_error_return(reason, return_code):
    if return_code == 0:
        raise CtxpException("Invalid return code. return_code must not be 0 (success) in error situation.")
    if not isinstance(return_code, int):
        raise CtxpException("Invalid return code. return_code must be integer, but got " + type(return_code))
    

def print_output(data: Any, output: str = "json", fields: str = None, file = sys.stdout):
    if type(data) is str:
        text = data
    elif isinstance(data, Exception):
        text = f"{type(data).__name__}: {data}"
    else:

        try:
            data = _convert_generator(data)
            _filter_fields(data, fields)

            if output == "json":
                text = json.dumps(data, default=vars, indent=4)
            elif output == "json-compact":
                text = json.dumps(data, default=vars)
            elif output == "yaml":
                import vhcs.common.ctxp as ctxp
                text = yaml.dump(ctxp.jsondot.plain(data))
            elif output == "text":
                if isinstance(data, list):
                    text = ""
                    for i in data:
                        line = i if type(i) is str else json.dumps(i)
                        text += line + "\n"
                elif isinstance(data, dict):
                    text = json.dumps(data, indent=4)
                else:
                    text = json.dumps(data, indent=4)
            else:
                raise Exception(f"Unexpected output format: {output}")
        except Exception as e:
            print("Fail converting object:", e, file=sys.stderr)
            text = data
    print(text, end="", file=file)

def print_error(error):
    if isinstance(error, httpx.HTTPStatusError):
        print(type(error).__name__, error, file=sys.stderr)
    elif isinstance(error, CtxpException):
        print(error, file=sys.stderr)
    else:
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def _convert_generator(data: Any):
    if isinstance(data, types.GeneratorType):
        return list(data)
    return data

def _filter_fields(obj: Any, fields: str):
    if not fields:
        return obj
    parts = fields.split(",")

    def _filter_obj(o):
        if not isinstance(o, dict):
            return o
        for k in list(o.keys()):
            if k not in parts:
                del o[k]
        return o

    if isinstance(obj, list):
        return list(map(_filter_obj, obj))
    return _filter_obj(obj)


def panic(reason: Any = None, code: int = 1):
    if isinstance(reason, CtxpException):
        text = str(reason)
    elif isinstance(reason, Exception):
        text = type(reason).__name__ + ": " + str(reason)
    else:
        text = reason
    print(text, file=sys.stderr)
    sys.exit(code)

def launch_text_editor(file_name : str, default_editor : str = None):
    if not default_editor:
        default_editor = 'vi'
    cmd = os.environ.get('EDITOR', default_editor) + ' ' + file_name
    subprocess.call(cmd, shell=True)


def choose(prompt: str, items: list, fn_get_text: Callable = None, selected = None):
    if len(items) == 0:
        panic(prompt + " ERROR: no item available.")

    if fn_get_text == None:
        fn_get_text = lambda t: str(t)
        
    if len(items) == 1:
        ret = items[0]
        print(prompt + " only one item available. Select by default: " + fn_get_text(ret))
        return ret
    
    choices = []
    size = len(items)
    for i in range(size):
        label = fn_get_text(items[i])
        #if label in choices:
        #    raise Exception("Problem with the provided fn_get_text: generates non-unique label. Item=" + label)
        choices.append(label)

    #hack workaround bug of the questionary lib
    selected_key = fn_get_text(selected) if selected else None
    k = questionary.select(prompt, choices, default=selected_key, show_selected=True).ask()
    if k == None:
        panic()
    for i in range(size):
        if k == choices[i]:
            return items[i]
    raise Exception("This is a bug and should not happen")

def input_array(prompt: str, default: list[str] = None):
    default_value = ",".join(default) if default else None
    
    input_value = click.prompt(prompt, default_value)
    if not input_value:
        return []
    parts = input_value.split(",")
    ret = []
    for p in parts:
        ret.append(p.strip())
    return ret

option_verbose = click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="Print debug logs",
)

option_output = click.option(
    "-o",
    "--output",
    type=click.Choice(["json", "json-compact", "yaml", "text"]),
    default="json",
    help="Specify output format",
)

option_field = click.option(
    "-f",
    "--field",
    type=str,
    required=False,
    help="Specify fields to output",
)

option_id_only = click.option(
    "--id-only/--full-object",
    type=bool,
    default=False,
    required=False,
    help="Output only the object, instead of the full data object",
)
