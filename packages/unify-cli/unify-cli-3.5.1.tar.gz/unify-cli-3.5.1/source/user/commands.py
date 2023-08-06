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
import json
import uuid
import string
import sys
import secrets
import random
import click
from tabulate import tabulate
from unify.apimanager import ApiManager
from unify.apiutils import tabulate_from_json
from source.common.commands import org_cluster_options, cluster_option

# Minimum password length for password generator
MIN_PW_LEN = 12

@click.group()
def user():
    """Group for the user related commands"""
    pass

@user.command('org-list')
@org_cluster_options
def org_user_list(org, remote):
    try:
        response = ApiManager(cluster=remote).orgs.retrieve_all_users_form_org(org)
        click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
        sys.exit(1)


@user.command('move')
@cluster_option
@click.option('--user', prompt="User Id", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--group', prompt="Group Id", hide_input=False, default=None, required=True, type=click.STRING)
def org_user_list(remote, user, group):
    try:
        response = ApiManager(cluster=remote).orgs.move_user_to_group(user_id=user, group_id=group)
        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
        sys.exit(1)


@user.command('group-list')
@cluster_option
@click.option('--table', '-t', is_flag=True, help="Print in table")
def group_list(remote, table):
    try:
        response = ApiManager(cluster=remote).orgs.get_all_groups()
        if table:
            response = tabulate_from_json(response["allGroups"])
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
        sys.exit(1)


@user.command('add')
@org_cluster_options
@click.option('--email', prompt="User Email", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--name', prompt="Person Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--role', prompt="User Role", hide_input=False, default='Contributor', required=False,
              type=click.Choice(['Admin', 'Contributor']))
def user_add(org, remote, email, name, role):
    try:
        response = ApiManager(cluster=remote).orgs.invite_user(
            org_id=org,
            email=email,
            name=name,
            role=role
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
        sys.exit(1)

@user.command('addserviceaccount')
@org_cluster_options
@click.option('--service_account_name', prompt="Service Account Name", hide_input=False, default=None, required=True,
              type=click.STRING)
@click.option('--service_account_id', prompt="Service Account ID (UUID format)", hide_input=False, default=None,
              required=True, type=click.STRING)
@click.option('--service_account_password', prompt="Service Account Password (UUIC format)", hide_input=True,
              default=None, required=True, type=click.STRING)
@click.option('--role', prompt="User Role", hide_input=False, default='Contributor', required=False)
def service_account_add_deprecated(org, remote, service_account_name, service_account_id, service_account_password, role):
    click.echo(click.style("This alias is deprecated and will be removed. "
                           + "See \"unify user machine add --help\" for updated syntax.", fg='red'))
    try:
        response = ApiManager(cluster=remote).orgs.invite_machine_user(
            org_id=org,
            fullname=service_account_name,
            id=service_account_id,
            password=service_account_password,
            role=role
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
        sys.exit(1)

@user.group()
def machine():
    """Sub-Group under user for the machine user related commands"""
    pass

@machine.command('add')
@org_cluster_options
@click.option('--name', help='Machine User Name, defaults to "machine-user-${account-id}"', default=None)
@click.option('--account-id', help="User ID (e.g. id from `unify user org-list`)", default=None)
@click.option('--password', help="Password", default=None)
@click.option('--role', help="User Role", default='Contributor')
def machine_user_add(org, remote, name, account_id, password, role):

    # Create the name, etc if not supplied
    show_generated_data = False
    if account_id is None:
        show_generated_data = True
        account_id = str(uuid.uuid4())
    if name is None:
        show_generated_data = True
        name = f"machine-user-{account_id}"
    if password is None:
        show_generated_data = True
        password = genValidPw(name)

    if show_generated_data:
        click.echo('Copy this and save it somewhere safe like a password manager, as you will not be able to retrieve it in the future!')
        click.echo(f'display name: {name}')
        click.echo(f'account_id: {account_id}')
        click.echo(f'password: {password}')

    try:
        response = ApiManager(cluster=remote).orgs.invite_machine_user(
            org_id=org,
            id=account_id,
            password=password,
            fullname=name,
            role=role
        )
        click.echo(click.style(str(response), bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), bold=True, fg='red'))
        sys.exit(1)

def genValidPw(username):
    """
    Generate a valid password

    This logic should probably live in the SDK, but keeping it here for now.
    """
    def hasRepeated(pw):
        """ Looks for any 3 char substring that is the same char"""
        try:
            # Use next instead of list comprehension so we only get the first
            next(pw[i:i+3] for i in range(len(pw) - 2) if pw[i:i+3][0] ==  pw[i:i+3][1] and pw[i:i+3][0] ==  pw[i:i+3][2])
            return True
        except:
            return False

    def s(ch):
       """ Successor to a character. i.e., char + 1 in c-like syntax"""
       return chr((ord(ch) + 1))

    def hasIncreasing(pw):
        """ Looks for any 3 char substring that is the same char"""
        try:
            # Use next instead of list comprehension so we only get the first
            next(pw[i:i+3] for i in range(len(pw) - 2) if s(pw[i:i+3][0]) ==  pw[i:i+3][1] and s(pw[i:i+3][1]) ==  pw[i:i+3][2])
            return True
        except:
            return False

    def isValid(password):
        """ validates a password using the same logic as: https://github.com/ElementAnalytics/element-workbench/blob/main/backend/workbench/src/main/scala/com/elementanalytics/util/PasswordValidator.scala
        """
        if len(password) < MIN_PW_LEN:
            return False
        if username in password:
            return False
        if hasRepeated(password):
            return False
        if hasIncreasing(password):
            return False

        return True

    while True:
        password = secrets.token_urlsafe(48)
        if isValid(password):
            return password


@machine.command('set-password')
@org_cluster_options
@click.option('--user', help="Machine User ID", required=True)
@click.option('--password', help="New Password", required=True)
def set_machine_user_password(org, remote, user, password):
    try:
        response = ApiManager(cluster=remote).orgs.change_machine_user_password(org_id=org, id=user, password=password)
        click.echo(click.style(json.dumps(response), bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), bold=True, fg='red'))
        sys.exit(1)
