from automation_base.config import Timeout
from automation_base.ui_base.web_base import By
from tests.frontend.web.pages.base_page import BasePage
from tests.frontend.web.pages.components.top_nav_bar import TopNavBar


class ProductDetails(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.locators.update({
            "product_title": (By.ID, "title"),
            "product_image": (By.ID, "imgTagWrapperId")
        })
        self.driver_base.wait_for_element_to_be_available('product_title', Timeout.XL)
        self.top_nav_bar = self.create(TopNavBar)
