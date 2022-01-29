from automation_base.config import Timeout
from automation_base.ui_base.web_base import By
from tests.frontend.web.pages.base_page import BasePage
from tests.frontend.web.pages.components.top_nav_bar import TopNavBar


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.locators.update({
            "main_carousel": (By.ID, "desktop-banner")
        })
        self.wait_for_element_to_be_clickable('main_carousel', Timeout.XL)
        self.top_nav_bar = self.create(TopNavBar)
