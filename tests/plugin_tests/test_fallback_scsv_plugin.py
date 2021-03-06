import unittest

import logging

from sslyze.plugins.fallback_scsv_plugin import FallbackScsvPlugin, FallbackScsvScanCommand
from sslyze.server_connectivity import ServerConnectivityInfo
from tests.plugin_tests.openssl_server import NotOnLinux64Error
from tests.plugin_tests.openssl_server import VulnerableOpenSslServer


class FallbackScsvPluginTestCase(unittest.TestCase):

    def test_fallback_good(self):
        server_info = ServerConnectivityInfo(hostname=u'www.google.com')
        server_info.test_connectivity_to_server()

        plugin = FallbackScsvPlugin()
        plugin_result = plugin.process_task(server_info, FallbackScsvScanCommand())

        self.assertTrue(plugin_result.supports_fallback_scsv)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_fallback_bad(self):
        try:
            server = VulnerableOpenSslServer(port=8010)
        except NotOnLinux64Error:
            # The test suite only has the vulnerable OpenSSL version compiled for Linux 64 bits
            logging.warning('WARNING: Not on Linux - skipping test_fallback_bad() test')
            return
        server.start()

        server_info = ServerConnectivityInfo(hostname=server.hostname, ip_address=server.ip_address,  port=server.port)
        server_info.test_connectivity_to_server()

        plugin = FallbackScsvPlugin()
        plugin_result = plugin.process_task(server_info, FallbackScsvScanCommand())
        server.terminate()

        self.assertFalse(plugin_result.supports_fallback_scsv)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())
