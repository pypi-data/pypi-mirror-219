"""
    Koverse Data Platform (KDP) API

    The KDP API is a REST API that can be used to create, access, and update data in KDP Workspaces  # noqa: E501

    The version of the OpenAPI document: 4.69.0
    Generated by: https://openapi-generator.tech
"""


import unittest

import kdp_api
from kdp_api.api.audit_log_configs_api import AuditLogConfigsApi  # noqa: E501


class TestAuditLogConfigsApi(unittest.TestCase):
    """AuditLogConfigsApi unit test stubs"""

    def setUp(self):
        self.api = AuditLogConfigsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_all_auditlog_configurations(self):
        """Test case for get_all_auditlog_configurations

        Get audit log configuration  # noqa: E501
        """
        pass

    def test_patch_auditlog_configuration(self):
        """Test case for patch_auditlog_configuration

        Patch audit log configuration of a workspace  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
