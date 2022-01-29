from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait

from automation_base.config import ApplicationUtils
from automation_base.singleton import Singleton


class DriverBase(object, metaclass=Singleton):
    def __init__(self, driver, locators=None):
        self.driver = driver
        self.locators = locators

    def find_element(self, element_name, format_options=None):
        """
        Searches for the given element in the DOM
        :param element_name:    String      Name of the element being searched
        :param format_options:  Opt.Param   List of parameters to format the locator
        :return:                Element     Instance of the element searched
        """
        try:
            element = self.driver.find_element(*self.format_locator(element_name, format_options))
        except StaleElementReferenceException:
            element = self.driver.find_element(*self.format_locator(element_name, format_options))
        return element

    def format_locator(self, element_name, format_options=None):
        """
        Formats a dynamic locator based in the options
        :param element_name:    String      Element name to find the locator in the Locators dict
        :param format_options:  Opt.Param   List of parameters to format the locator
        :return:                List        Formatted locator to find the element
        """
        locator = list(self.locators[element_name])
        format_options = [format_options] if isinstance(format_options, str) else format_options
        if format_options and len(locator) > 1:
            locator[1] = locator[1].format(*format_options)
        return locator

    def is_child_element_displayed(self, parent_element, element_name, format_options=None):
        """
        Check if a specific element is displayed
        :param parent_element:  WebElement  Parent element to find the child from
        :param element_name:    String      Element name to find the locator in Locators dict,
        :param format_options:  Opt.Param   List of parameters to format the locator
        :return:                Boolean     True if the element is displayed, False otherwise
        """
        return parent_element.find_element(
            *self.format_locator(element_name, format_options)).is_displayed()

    def is_element_displayed(self, element_name, format_options=None):
        """
        Check if a specific element is displayed
        :param element_name:    String      Element name to find the locator in Locators dict
        :param format_options:  Opt.Param   List of parameters to format the locator
        :return:                Boolean     True if the element is displayed, False otherwise
        """
        try:
            return self.find_element(element_name, format_options).is_displayed()
        except StaleElementReferenceException:
            return self.find_element(element_name, format_options).is_displayed()

    def wait_for_element_to_be_available(self, element_name, wait_time, format_options=None):
        """
        Wait until an specific element is available
        :param element_name:    String      Element name to wait for
        :param wait_time:       Int         Time to wait for the element to be available
        :param format_options:  Opt.Param   List of parameters to format the locator
        """
        WebDriverWait(self.driver, wait_time).until(
            lambda s: self.is_element_available(element_name, 0, format_options),
            f'The element {element_name} is not displayed after waiting for {wait_time} seconds')

    def wait_for_element_to_disappear(self, element_name, wait_time, format_options=None):
        """
        Wait until an specific element is not available
        :param element_name:    String      Element name to wait for
        :param wait_time:       Int         Time to wait for the element to disappear
        :param format_options:  Opt.Param   List of parameters to format the locator
        """
        WebDriverWait(self.driver, wait_time).until(
            lambda s: not self.is_element_available(element_name, 0, format_options),
            f'The element {element_name} is still available after waiting for {wait_time} seconds')

    def find_elements(self, element_name, wait_time=None, format_options=None):
        """
        Gets the list of available elements with a specific locator name
        :param element_name:    String      Element name to find the locator in Locators dict
        :param wait_time:       Opt.Integer Time to wait while searching for the element
        :param format_options:  Opt.Param   List of parameters to format the locator
        :return:                List        WebElements found for the given locator name
        """

        self.driver.implicitly_wait(wait_time or ApplicationUtils().get_timeout())
        elements = self.driver.find_elements(*self.format_locator(element_name, format_options))
        self.driver.implicitly_wait(ApplicationUtils().get_timeout())
        return elements

    def is_child_element_available(self, parent_element, element_name, wait_time=0,
                                   format_options=None):
        """
         Check if a specific element is available
         :param parent_element:  WebElement Parent element to find the child from
         :param element_name:    String         Element name to find the locator in Locators dict
         :param wait_time:       Integer        Time to wait for the element to be available
         :param format_options:  Opt.Param      List of parameters to format the locator
         :return:                Boolean        True if the element is available, False otherwise
         """
        self.driver.implicitly_wait(wait_time)
        try:
            return self.is_child_element_displayed(parent_element, element_name,
                                                   format_options)
        except NoSuchElementException:
            return False

        finally:
            self.driver.implicitly_wait(ApplicationUtils().get_timeout())

    def is_element_available(self, element_name, wait_time=0.1, format_options=None):
        """
         Check if a specific element is available
         :param element_name:    String         Element name to find the locator in Locators dict
         :param wait_time:       Integer        Time to wait for the element to be available
         :param format_options:  Opt.Param      List of parameters to format the locator
         :return:                Boolean        True if the element is available, False otherwise
         """
        self.driver.implicitly_wait(wait_time)
        try:
            return self.is_element_displayed(element_name, format_options) and \
                   self.find_element(element_name, format_options).is_enabled()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

        finally:
            self.driver.implicitly_wait(ApplicationUtils().get_timeout())

    def get_element_text(self, element_name, format_options=None):
        """
        Retrieve the specific text for a given element name
        :param element_name:    String      Element name to find the locator in the Locators dict
        :param format_options:  Opt.Param   List of parameters to format the locator
        :return:
        """
        try:
            return self.find_element(element_name, format_options).text
        except StaleElementReferenceException:
            return self.find_element(element_name, format_options).text

    def get_element_attribute(self, element_name, attribute, format_options=None):
        """
        Retrieve the specific attribute value for a given element name
        :param element_name:    String      Element name to find the locator in the Locators dict
        :param attribute:       String      Element attribute to get the value
        :param format_options:  Opt.Param   List of parameters to format the locator
        :return:
        """
        return self.find_element(element_name, format_options).get_attribute(attribute)

    def wait_for_element_to_have_text(self, element_name, expected_text, wait_time, get_text_method,
                                      format_options=None):
        """
        Wait until an specific element has the given text
        :param element_name:    String      Element name to wait for
        :param expected_text:   String      Text to wait for the element to have
        :param wait_time:       Int         Time to wait for the element to be available
        :param get_text_method: Method      For tests in the webapp should be automation_base.get_text,
                                            For tests in the mobile app should be get_element_name
        :param format_options:  Opt.Param   List of parameters to format the locator
        """
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda s: get_text_method(element_name, format_options=format_options) == expected_text,
                f'The element {element_name} text was not the expected after waiting for {wait_time} seconds')
        except StaleElementReferenceException:
            WebDriverWait(self.driver, wait_time).until(
                lambda s: get_text_method(element_name, format_options=format_options) == expected_text,
                f'The element {element_name} text was not the expected after waiting for {wait_time} seconds')

    def wait_for_element_to_be_focused(self, element_name, wait_time, format_options):
        """
        Waits until the element attribute 'focused' is true
        :param element_name:    String      Name of the element being searched
        :param wait_time:       Int         Time to wait for the element to be available
        :param format_options:  Opt.Param   List of parameters to format the locator
        """
        WebDriverWait(self.driver, wait_time).until(
            lambda s: self.get_element_attribute(element_name, 'focused', format_options) == 'true',
            f'The element {element_name} is not displayed after waiting for {wait_time} seconds')

    def wait_for_context(self, wait_time, expected_context):
        """
        Waits until a given context exists within the driver
        :param wait_time:        Int         Time to wait for the context to be available
        :param expected_context: String      App context name
        """
        WebDriverWait(self.driver, wait_time).until(
            lambda s: expected_context in self.driver.contexts,
            f'The context {expected_context} is not available after waiting for {wait_time} seconds')
