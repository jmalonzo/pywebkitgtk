
import webkit
from webkit import NetworkRequest

import gobject
import unittest

class TestNetworkRequest(unittest.TestCase):

    def setUp(self):
        self.request = webkit.NetworkRequest()

    def testsettergetter(self):
        self.request.set_uri("http://example.com/index.php")
        self.assertEqual("http://example.com/index.php", self.request.get_uri())

    def testdefaultinitvalue(self):
        self.assertEqual("about:blank", self.request.get_uri())

    def testsetproxy(self):
        webkit.set_proxy("http://localhost:8080")
        # we're still OK.
        self.assertTrue(True)

    def tearDown(self):
        del self.request

if __name__ == '__main__':
    unittest.main()
