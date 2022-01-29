import random

from selenium.webdriver.support.wait import WebDriverWait

from automation_base.config import Timeout
from automation_base.ui_base.web_base import By
from tests.frontend.web.pages.base_page import BasePage
from tests.frontend.web.pages.components.top_nav_bar import TopNavBar
from tests.frontend.web.pages.product_details import ProductDetails


class ResultsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.locators.update({
            "search_results": (By.CSS_SELECTOR, "div[data-component-type=s-search-result] h2>a"),
            "search_text": (By.ID, "twotabsearchtextbox"),
            "search_submit_button": (By.ID, "nav-search-submit-button")
        })
        WebDriverWait(self.driver, Timeout.XL).until(
            lambda x: len(self.driver_base.find_elements('search_results', Timeout.XXS)) > 0,
            "Error after waiting for results page to load")
        self.top_nav_bar = self.create(TopNavBar)
        self.results = self.driver_base.find_elements('search_results')

    def get_search_results(self):
        """
        Get all the results text found while doing the search
        @return: List   Search results
        """
        return [result.text for result in self.results]

    def open_product(self, select_type='random', select_value=None):
        """
        Open an specific product, it can be a random product, a specific text product or a product in the given position
        @param select_type:     Optional.String Type of select to use it can be one of the
                                                following [random, position, value]. DefaultValue:random
        @param select_value:    Optional.String Result to select that matches the given value. DefaultValue:None
        @return:            ProductDetails  Page instance of the opened product
        """
        if select_type == 'value':
            for result in self.results:
                if select_value.lower() in result.text.lower():
                    result.click()
                    break
        elif select_value == 'position':
            self.results[select_value-1].click()
        else:
            random.choice(self.results).click()
        return self.create(ProductDetails)
