
from webkit import WebHistoryItem, WebBackForwardList, WebView

import gobject
import unittest

class TestWebBackForwardList (unittest.TestCase):
    """Test WebBackForwardList functions"""

    def setUp(self):
        gobject.threads_init()
        self.view = WebView()
        self.bf_list = self.view.get_back_forward_list()

    def testadditem(self):
        item =  WebHistoryItem(uri="http://example.com/", title="Example1")
        self.bf_list.add_item(item)
        self.assertEqual(item, self.bf_list.get_current_item())
        currentItem = self.bf_list.get_current_item()
        self.assertEqual("Example1", currentItem.get_title())
        self.assertEqual("http://example.com/", currentItem.get_uri())

    def testbackforwardlistwithlimit(self):
        item1 =  WebHistoryItem(uri="http://example.com/1/", title="Example1")
        item2 =  WebHistoryItem(uri="http://example.com/2/", title="Example2")
        item3 =  WebHistoryItem(uri="http://example.com/3/", title="Example3")
        item4 =  WebHistoryItem(uri="http://example.com/4/", title="Example4")
        self.bf_list.add_item(item1)
        self.bf_list.add_item(item2)
        self.bf_list.add_item(item3)
        self.bf_list.add_item(item4)
        backList = list()
        backList = self.bf_list.get_back_list_with_limit(10)
        self.assertTrue(backList is not None)
        self.assertEqual("Example4", self.bf_list.get_current_item().get_title())
        self.assertEqual("Example3", backList[0].props.title)
        self.assertEqual("Example2", backList[1].props.title)
        self.assertEqual("Example1", backList[2].props.title)
        self.bf_list.go_to_item(item1)
        self.assertEqual(self.bf_list.get_current_item().get_title(), item1.get_title())
        forwardList = list()
        forwardList = self.bf_list.get_forward_list_with_limit(10)
        self.assertTrue(forwardList is not None)
        self.assertEqual("Example4", forwardList[0].props.title)
        self.assertEqual("Example3", forwardList[1].props.title)
        self.assertEqual("Example2", forwardList[2].props.title)

    def testclearbackforwardlist(self):
        item1 =  WebHistoryItem(uri="http://example.com/1/", title="Example1")
        item2 =  WebHistoryItem(uri="http://example.com/2/", title="Example2")

        self.bf_list.set_limit(0)
        self.bf_list.set_limit(1)
        self.bf_list.add_item(item2)
        self.assertEqual(self.bf_list.get_back_length(), 0)
        self.assertEqual(self.bf_list.get_forward_length(), 0)
        self.assertEqual(self.bf_list.get_current_item(), item2)

    def tearDown(self):
        # nothing here.
        pass

if __name__ == '__main__':
    unittest.main()
