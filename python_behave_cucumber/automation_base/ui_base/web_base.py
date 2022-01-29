from time import sleep

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from automation_base.singleton import Singleton
from automation_base.ui_base.base import PageObject
from automation_base.config import Timeout


class WebBase(PageObject):

    def __init__(self, driver, locators):
        super().__init__(driver, locators)

    def click_button(self, button_name, format_options=None):
        """
        Clicks on a specific button by updating the locator based on the given options
        :param button_name:        String      Name of the button to be clicked
        :param format_options:     Opt.Params  List of parameters to format the locator
        """
        try:
            element = self.scroll_to_element(button_name, format_options)
            element.click()
        except StaleElementReferenceException:
            element = self.scroll_to_element(button_name, format_options)
            element.click()

    def set_element_text(self, element_name, text, format_options=None):
        """
        Clear and then set a specific text in the specific input field
        :param element_name:    String      Element name to find the locator in the Locators dict
        :param text:            String      Data to set in the element specified
        :param format_options:  Opt.Param   List of parameters to format the locator
        """
        element = self.driver_base.find_element(element_name, format_options)
        element.clear()
        element.send_keys(text)

    def wait_for_element_to_be_clickable(self, element_name, wait_time, format_options=None):
        try:
            WebDriverWait(self.driver, wait_time).until(expected_conditions.element_to_be_clickable(
                self.driver_base.format_locator(element_name, format_options)))
        except StaleElementReferenceException:
            WebDriverWait(self.driver, wait_time).until(expected_conditions.element_to_be_clickable(
                self.driver_base.format_locator(element_name, format_options)))

    def open(self, url):
        self.driver.get(url)

    def scroll_to_element(self, element_name, format_options=None):
        """
        Scroll for an element to be visible.
        :param element_name:    String      Element name to find the locator in the Locators dict
        :param format_options:  Opt.Param   List of parameters to format the locator
        """
        self.driver_base.wait_for_element_to_be_available(element_name, Timeout.M, format_options)
        element = self.driver_base.find_element(element_name, format_options)

        # Scroll the element to be at the top left of the screen except when the header or drawer are displayed
        # For these cases perform the scroll right after these elements
        x = element.location['x'] #- drawer_element.size['width']
        y = element.location['y'] #- header_element.size['height']
        self.driver.execute_script("window.scrollTo(arguments[0],arguments[1]);", x, y)
        sleep(Timeout.XXS)
        self.wait_for_element_to_be_clickable(element_name, Timeout.M, format_options)
        return element