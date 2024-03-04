import os

import pydantic_settings

from wikipedia_tests.utils import file


class Config(pydantic_settings.BaseSettings):
    timeout: float = 10.0
    app: str = os.getenv('APP')
    app_wait_activity: str = os.getenv('APP_AWAIT_ACTIVITY')
    platform_name: str = os.getenv('PLATFORM_NAME')
    platform_version: str = os.getenv('PLATFORM_VERSION')
    remote_url: str = os.getenv('REMOTE_URL')
    device_name: str = os.getenv('DEVICE_NAME')

    def to_driver_options(self, context):
        from appium.options.android import UiAutomator2Options
        options = UiAutomator2Options()

        if context == 'bstack':
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('deviceName', self.device_name)
            options.set_capability('platformName', self.platform_name)
            options.set_capability('platformVersion', self.platform_version)
            options.set_capability('appWaitActivity', self.app_wait_activity)
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
        elif context == 'local_real':
            options.set_capability('platformName', self.platform_name)
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('app', file.abs_path_from_project(self.app))
            options.set_capability('appWaitActivity', self.app_wait_activity)
        elif context == 'local_emulator':
            options.set_capability('platformName', self.platform_name)
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('app', file.abs_path_from_project(self.app))
            options.set_capability('appWaitActivity', self.app_wait_activity)

        return options


config = Config()
