from automation_base.ui_base.web_base import By
from tests.frontend.web.pages.base_page import BasePage


class TopNavBar(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.locators.update({
            "today_deals": (By.XPATH, "//div[@id='nav-xshop']/a[contains(text(), 'Today\'s Deals')]"),
            "search_text": (By.ID, "twotabsearchtextbox"),
            "search_submit_button": (By.ID, "nav-search-submit-button")
        })

    def perform_search(self, search_value):
        """
        Searches for the given value
        @param search_value:    String      Text to search for
        @return:                ResultsPage Results Page instance
        """
        from tests.frontend.web.pages.results_page import ResultsPage
        self.set_element_text('search_text', search_value)
        self.click_button('search_submit_button')
        return self.create(ResultsPage)
