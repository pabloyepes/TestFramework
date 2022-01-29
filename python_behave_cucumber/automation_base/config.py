import configparser
import os


class Timeout:
    XXS = 1
    XS = 3
    S = 5
    M = 10
    L = 30
    XL = 60
    XXL = 90
    XXXL = 240


class ConfigurationParser(object):
    def __init__(self):
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read_file(open('setup.cfg'))

    def get_driver_name(self):
        return self._config_parser.get('driver', 'driver_name')

    def get_timeout(self):
        return self._config_parser.get('driver', 'timeout')

    def get_idle_timeout(self):
        return self._config_parser.get('driver', 'idle_timeout')

    def get_appium_device(self):
        return self._config_parser.get('appium', 'device')

    def get_app_package(self):
        return self._config_parser.get('appium', 'app_package')

    def get_app_activity(self):
        return self._config_parser.get('appium', 'app_activity')

    def get_appium_device_name(self):
        return self._config_parser.get('appium', 'device_name')

    def get_hub_url(self):
        return self._config_parser.get('appium', 'hub_url')

    def get_login_token(self):
        return self._config_parser.get('test', 'login_token')

    def get_user_password(self, user):
        return self._config_parser.get('test', f'{user}_password')

    def get_user_email(self, user):
        return self._config_parser.get('test', f'{user}_user')

    def get_test_environment(self):
        return self._config_parser.get('test', f'test_environment')


class ApplicationUtils(object):

    def __init__(self):
        self.configuration_parser = ConfigurationParser()

    @staticmethod
    def _get(option1, option2_as_function, function_param=None):
        r = os.environ.get(option1)
        if not (r and r != ''):
            if function_param:
                r = option2_as_function(function_param)
            else:
                r = option2_as_function()
        return r

    def get_driver_name(self):
        return self._get('DRIVER_NAME', self.configuration_parser.get_driver_name)

    def get_timeout(self):
        return int(self._get('TIMEOUT', self.configuration_parser.get_timeout))

    def get_idle_timeout(self):
        return int(self._get('IDLE_TIMEOUT', self.configuration_parser.get_idle_timeout))

    def get_appium_device(self):
        return self._get('DEVICE', self.configuration_parser.get_appium_device)

    def get_hub_url(self):
        return self._get('HUB_URL', self.configuration_parser.get_hub_url)

    def get_app_package(self):
        return self._get('APP_PACKAGE', self.configuration_parser.get_app_package)

    def get_app_activity(self):
        return self._get('APP_ACTIVITY', self.configuration_parser.get_app_activity)

    def get_appium_device_name(self):
        return self._get('DEVICE_NAME', self.configuration_parser.get_appium_device_name)

    def get_login_token(self):
        return self._get('LOGIN_TOKEN', self.configuration_parser.get_login_token)

    def get_user_password(self, user):
        return self._get(f'{user}_PASSWORD', self.configuration_parser.get_user_password, user)

    def get_user_email(self, user):
        return self._get(f'{user}_USER', self.configuration_parser.get_user_email, user)

    def get_test_environment(self):
        return self._get('TEST_ENVIRONMENT', self.configuration_parser.get_test_environment)
