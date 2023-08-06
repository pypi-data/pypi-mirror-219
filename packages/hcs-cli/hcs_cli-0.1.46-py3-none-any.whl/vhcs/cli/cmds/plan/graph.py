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
@click.option("--view/--output-only", "-v", type=bool, default=True, help="If view mode is specified, open browser to view the graph.")
@click.option("--simplify/--full", "-v", type=bool, default=True, help="In simplified mode, show minimal edges. In full mode, show all edges.")
def graph(file, view: bool, simplify: bool):
    """Generate a graph view of the deployment, in Graphviz format."""

    try:
        data, extra = util.load_plan(file)
        g = plan.graph(data, extra, simplify)
        if view:
            _view_graph(g.source)
        return g.source
    except (FileNotFoundError, plan.PlanException) as e:
        return str(e), 1
    

def _view_graph(src):
    import urllib.parse
    import webbrowser
    url = 'https://dreampuf.github.io/GraphvizOnline/#' + urllib.parse.quote(src)
    webbrowser.open(url, new=0, autoraise=True)