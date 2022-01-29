from urllib.error import URLError

from appium import webdriver as appium_webdriver
from selenium import webdriver as selenium_webdriver

from webdriver_manager.chrome import ChromeDriverManager
from automation_base.config import ApplicationUtils


def create_appium_driver(clean_storage=False):
    """
    Creates an Appium WebDriver instance
    """
    app_utils = ApplicationUtils()
    device = app_utils.get_appium_device().lower()
    caps = {
        'platformName': device,
        'noReset': not clean_storage,
        "automationName": "uiautomator2",
        "deviceName": app_utils.get_appium_device_name(),
        'unicodeKeyboard': True,
        'resetKeyboard': True,
        'newCommandTimeout': app_utils.get_idle_timeout(),
        'waitForIdleTimeout': app_utils.get_idle_timeout(),
        'retryBackoffTime': 1000,
        'appPackage': app_utils.get_app_package(),
        'appActivity': app_utils.get_app_activity(),
    }

    try:
        driver = appium_webdriver.Remote(f'{app_utils.get_hub_url()}',
                                         desired_capabilities=caps)
    except URLError as err:
        raise URLError(
            f'Could not create GRID driver [Hub URL: {app_utils.get_hub_url()}] | {err.reason}')

    driver.implicitly_wait(app_utils.get_timeout())

    return driver


def get_chrome_options():
    chrome_options = selenium_webdriver.ChromeOptions()
    return chrome_options


def _create_chrome_driver():
    driver = selenium_webdriver.Chrome(ChromeDriverManager().install(), chrome_options=get_chrome_options())
    driver.maximize_window()
    return driver


def get_firefox_profile():
    profile = selenium_webdriver.FirefoxProfile()
    return profile


def _create_firefox_driver():
    return selenium_webdriver.Firefox(firefox_profile=get_firefox_profile())


def create(driver_name):
    driver_handler = {
        'chrome': _create_chrome_driver,
        'firefox': _create_firefox_driver,
        'appium': create_appium_driver
    }

    driver = driver_handler[driver_name]()

    return driver
