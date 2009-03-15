
from webkit import WebFrame, WebView

import gobject
import unittest

class TestWebFrame(unittest.TestCase):

    def setUp(self):
        gobject.threads_init()
        self.view = WebView()
        self.mainFrame = self.view.get_main_frame()

    def testloaduri(self):
        self.mainFrame.load_uri("about:blank")
        self.assertEqual("about:blank", self.mainFrame.get_uri());


    def tearDown(self):
        self.view.destroy()

if __name__ == '__main__':
    unittest.main()
