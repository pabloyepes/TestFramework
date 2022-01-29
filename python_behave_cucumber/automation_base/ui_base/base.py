from automation_base.singleton import Singleton
from automation_base.ui_base import driver
from automation_base.ui_base.driver_base import DriverBase


class PageObjectFactory(object, metaclass=Singleton):
    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    def create(self, page_object_type, **kwargs):
        return page_object_type(self.driver, **kwargs)


class PageObject(object):
    def __init__(self, driver, locators=None):
        page_factory = PageObjectFactory()
        page_factory.driver = driver
        #page_factory._driver = driver
        self.driver_base = DriverBase(driver, locators)

    @property
    def driver(self):
        return self.driver_base.driver

    def create(self, page_object_type, **kwargs):
        return PageObjectFactory().create(page_object_type, **kwargs)
