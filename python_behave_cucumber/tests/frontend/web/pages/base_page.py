from automation_base.config import Timeout
from automation_base.ui_base.web_base import By, WebBase


class BasePage(WebBase):

    def __init__(self, driver):
        self.locators = {}
        super().__init__(driver, self.locators)
        self.locators = self.driver_base.locators
        self.locators.update({
            "nav_logo": (By.ID, "nav-logo-sprites")
        })
