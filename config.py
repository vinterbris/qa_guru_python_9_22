import os

import pydantic_settings
from dotenv import load_dotenv

from tests.conftest import context

load_dotenv('.env')


class Config(pydantic_settings.BaseSettings):
    context: str
    timeout: float = 10.0

    app: str = os.getenv('APP')
    appWaitActivity: str = os.getenv('APP_AWAIT_ACTIVITI')

    remote_url: str = os.getenv('REMOTE_URL')
    android_platform_version: str = os.getenv('PLATFORM_VERSION')
    device_name: str = os.getenv('DEVICE_NAME')
    browserstack_app_url: str = os.getenv('APP_URL')

    def to_driver_options(self):
        from appium.options.android import UiAutomator2Options
        options = UiAutomator2Options()

        if context == 'bstack':
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('deviceName', self.device_name)
            options.set_capability('platformName', self.platformName)
            options.set_capability('platformVersion', self.platformVersion)
            options.set_capability('appWaitActivity', self.appWaitActivity)
            options.set_capability('app', self.app)
            options.set_capability(
                'bstack:options', {
                    'projectName': 'First Python project',
                    'buildName': 'browserstack-build-1',
                    'sessionName': 'BStack first_test',
                    'userName': os.getenv('USER_NAME'),
                    'accessKey': os.getenv('ACCESSKEY'),
                },
            )

        return options


config = Config(context='bstack')
