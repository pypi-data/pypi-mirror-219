"""
    Koverse Data Platform (KDP) API

    The KDP API is a REST API that can be used to create, access, and update data in KDP Workspaces  # noqa: E501

    The version of the OpenAPI document: 4.69.0
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import kdp_api
from kdp_api.model.workspace_subscription import WorkspaceSubscription
globals()['WorkspaceSubscription'] = WorkspaceSubscription
from kdp_api.model.workspace import Workspace


class TestWorkspace(unittest.TestCase):
    """Workspace unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWorkspace(self):
        """Test Workspace"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Workspace()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
