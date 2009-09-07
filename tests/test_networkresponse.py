
import webkit
from webkit import NetworkResponse

import gobject
import unittest

class TestWebView(unittest.TestCase):

    def setUp(self):
        self.response = webkit.NetworkResponse()

    def testsettergetter(self):
        self.response.set_uri("http://example.com/index.php")
        self.assertEqual("http://example.com/index.php", self.response.get_uri())

    def testdefaultinitvalue(self):
        self.assertEqual("about:blank", self.response.get_uri())

    def tearDown(self):
        del self.response

if __name__ == '__main__':
    unittest.main()
