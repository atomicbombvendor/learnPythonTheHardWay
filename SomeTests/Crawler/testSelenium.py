import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        element = driver.find_element_by_xpath("//select[@name='name']")
        all_options = element.find_element_by_tag_name("option")
        for option in all_options:
            print("value is: %s" % option.get_attribute("value"))
            option.click()
        select = Select(driver.find_element_by_name('name'))
        # select.select_by_index(index=)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()