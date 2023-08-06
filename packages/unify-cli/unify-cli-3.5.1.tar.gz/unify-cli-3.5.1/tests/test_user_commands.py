# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import uuid
import unittest
import logging
from click.testing import CliRunner

from source.cluster.commands import add_cluster
from source.cluster.commands import disconnect_cluster
from source.cluster.commands import login
from source.user.commands import machine_user_add as service_account_add, service_account_add_deprecated, genValidPw
from tests.properties import Properties

from tests import test_org
from tests import test_pipeline

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Helpers
def assert_n_times(times, func, *arg_func, last_ex=None):
    recompute = lambda f: f() if type(f).__name__ == 'function' else f

    if times <= 0:
        raise last_ex

    try:
        func(*list(map(recompute, arg_func)))
    except Exception as e:
        return assert_n_times(times - 1, func, *arg_func, last_ex=e)

# Test Cases
class UserTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()
        cls.cluster_name = str(uuid.uuid4())[:4]
        cls.props = Properties()

        params = [
            "--remote", cls.props.api_url,
            "--username", cls.props.user_name,
            "--password", cls.props.user_password,
            "--name", cls.cluster_name,
            "--assetsync", True
        ]

        cls.runner.invoke(add_cluster, params)
        cls.runner.invoke(login, ["--remote", cls.cluster_name])

    def test_service_account_add_admin(self):
        name = str(uuid.uuid4())
        def params():
            return [
                        "--remote", self.cluster_name,
                        "--org", test_org,
                        "--service_account_name",name,
                        "--service_account_id", str(uuid.uuid4()),
                        "--service_account_password", genValidPw(name),
                        "--role", 'Admin'
                    ]

        def t(params):
            add_user_result = self.runner.invoke(service_account_add_deprecated, params)
            self.assertEqual(add_user_result.exit_code, 0, add_user_result.output)

        assert_n_times(2, t, params)


    def test_service_account_add_contributor(self):
        name = str(uuid.uuid4())

        def params():
            return [
                        "--remote", self.cluster_name,
                        "--org", test_org,
                        "--service_account_name",name,
                        "--service_account_id", str(uuid.uuid4()),
                        "--service_account_password", genValidPw(name),
                        "--role", 'Contributor'
                    ]

        def t(params):
            add_user_result = self.runner.invoke(service_account_add_deprecated, params)
            self.assertEqual(add_user_result.exit_code, 0, add_user_result.output)

        assert_n_times(2, t, params)

    def test_service_account_add_invalid(self):
        name = str(uuid.uuid4())
        def params():
            return [
                        "--remote", self.cluster_name,
                        "--org", test_org,
                        "--service_account_name",name,
                        "--service_account_id", str(uuid.uuid4()),
                        "--service_account_password", genValidPw(name),
                        "--role", str(uuid.uuid4())
                    ]

        def t(params):
            add_user_result = self.runner.invoke(service_account_add_deprecated, params)
            logging.debug(add_user_result)
            self.assertNotEquals(add_user_result.exit_code, 0, add_user_result.output)

        assert_n_times(2, t, params)

    @unittest.skip('Not yet implemented')
    def test_add_admin_fail(self):
        """
        Try to create an admin user by a non-admin user. This should fail as
        users should not be able to grant more permissions than they have.
        """
        fail('not implemented')

    @unittest.skip('Not yet implemented')
    def test_add_generate_user_pass(self):
        """
        Create a user without specifying the name, id, or password.

        Machine user should be created and values should be printed to stdout.
        """

        fail('not implemented')


    @classmethod
    def tearDownClass(cls):
        cls.runner.invoke(disconnect_cluster, ["--remote", cls.cluster_name, "-y"])
