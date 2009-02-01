
import webkit
import unittest

class TestWebNavigationAction (unittest.TestCase):
    """Test WebNavigationAction functions"""

    def setUp (self):
        """set up test"""
        self.navigation_action = webkit.WebNavigationAction()

    def testsetreason (self):
        """test for WebNavigationAction.set_reason/get_reason overrides"""
        reasons = ["link-clicked","reload","form-submitted","back-forward","form-resubmitted","other"]
        for r in reasons:
            self.navigation_action.set_reason(r)
            self.assertEqual(r, self.navigation_action.get_reason().value_nick)

    def testoriginaluri (self):
        """test WebNavigationAction.set/get_original_uri"""
        self.navigation_action.set_original_uri("http://www.google.com")
        self.assertEqual("http://www.google.com", self.navigation_action.get_original_uri())

if __name__ == '__main__':
   unittest.main()
