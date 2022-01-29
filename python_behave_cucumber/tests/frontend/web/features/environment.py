from automation_base.ui_base import driver
from automation_base.config import ApplicationUtils
from env_config import EnvironmentConfig
from tests.frontend.web.pages.base_page import BasePage
from tests.frontend.web.pages.home_page import HomePage
from utils import Utils


def before_scenario(context, scenario):
    context.base_url = EnvironmentConfig.amazon()[ApplicationUtils().get_test_environment()]
    context.driver = driver.create('chrome')
    context.page = BasePage(context.driver)
    context.page.open(context.base_url)
    context.page = context.page.create(HomePage)


def after_scenario(context, scenario):
    tags = Utils().get_scenario_tags(scenario)
    context.page.driver.quit()
