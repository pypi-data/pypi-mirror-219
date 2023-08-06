#!/usr/bin/env python

# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import click
import pandas as pd
from unify.apimanager import ApiManager
from unify.generalutils import json_to_csv

from source.common.commands import org_cluster_options
from datetime import datetime
import threading


@click.group()
def datastream():
    """Group for datastream commands"""


ts_schema = {
    "columns": [
        {
            "header": "name",
            "column": {
                "type": "text",
                "properties": {
                    "optional": False,
                    "datasets.v1.columnType": "Normal"
                }
            }
        },
        {
            "header": "timestamp",
            "column": {
                "type": "timestamp",
                "properties": {
                    "optional": False,
                    "datasets.v1.columnType": "Normal"
                }
            }
        },
        {
            "header": "value",
            "column": {
                "type": "double",
                "properties": {
                    "optional": False,
                    "datasets.v1.columnType": "Normal"
                }
            }
        },
        {
            "header": "questionable",
            "column": {
                "type": "text",
                "properties": {
                    "optional": False,
                    "datasets.v1.columnType": "Normal"
                }
            }
        },
        {
            "header": "status",
            "column": {
                "type": "text",
                "properties": {
                    "optional": False,
                    "datasets.v1.columnType": "Normal"
                }
            }
        }
    ],
    "properties": {}
}
def gen_ts(tag, timestamp):
    return {
        "name": tag,
        "timestamp": timestamp,
        "value": random.uniform(1.5, 100.5),
        "questionable": str(random.choice([True, False])),
        "status": random.choice(["Good", "Bad"])
    }
@datastream.command('simulate')
@org_cluster_options
@click.option('--name', prompt="Datastream Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--interval', prompt="Interval in Seconds", hide_input=False, default=5, required=True,type=click.INT)
def simulate_datastream(org, remote, name, interval, maxEvent=10000):
    """This simulator generate time series data as datastream. \n Enter end or quit to end the simulator. \n The max event is can generate is 10000"""
    try:
        api_manager = ApiManager(cluster=remote)
        dataset_id = api_manager.sources.create_command(
            org_id=org,
            schema=ts_schema,
            name=name,
            facets=[],
            description="datastream test",
            cause=[],
            is_stream=True)['uuid']
        model_file_path = os.path.join(os.path.dirname(__file__), 'tags.csv')
        pi_tags = pd.read_csv(model_file_path)['name'].tolist()
        flag = 0

        def gen_event(i):
            if flag == 1 or i > maxEvent:
                print("exit the simulator!")
                click.echo(click.style(str(dataset_id), blink=False, bold=True, fg='green'))
            else:
                print("Create {}th event".format(i))
                threading.Timer(interval, gen_event, [i + 1]).start()
                time = int(datetime.now().timestamp() * 1000000)
                pi_ts = map(lambda tag: gen_ts(tag, time), pi_tags)
                csv = json_to_csv(pi_ts)
                api_manager.sources.add_data_content_to_existing_source('ts', org, content=csv, data_set_id=dataset_id)

        gen_event(1)
        mm = input()
        if mm.lower() in ('end', 'quit'):
            flag = 1

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
