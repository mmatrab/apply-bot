import unittest

from selenium import webdriver

BROWSER_URL = 'http://browser:4444/wd/hub'
WP_URI = 'http://docker.wp.com/'


class Tests(unittest.TestCase):
    def test_smth(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor=BROWSER_URL, options=options)
        driver.get(WP_URI)
        print(driver.get_screenshot_as_file('/tmp/a.png'))
        driver.quit()

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(Tests))
    return test_suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=3).run(suite())
