import allure
import allure_commons
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from selene import browser, support

from config import config
from wikipedia_tests import utils
from wikipedia_tests.utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        required=False,
        default="bstack",
        choices=['bstack', 'local_real', 'local_emulator'],
    )


def pytest_configure(config):
    context = config.getoption("--context")
    load_dotenv(dotenv_path=f'.env.{context}')


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope='function', autouse=True)
def mobile_management_local(context):
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            config.remote_url,
            options=config.to_driver_options()
        )
    browser.config.timeout = config.timeout
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    options = UiAutomator2Options().load_capabilities({
        # 'deviceName': '2A191FDH200DSH',
        'app': config.app,
        'appWaitActivity': config.app_await_activity
    })

    options.set_capability('app', (
        config.app if config.app.startswith('/') or config.app.startswith('bs://')
        else utils.file.abs_path_from_project(config.app)
    ))

    yield

    attach.attach_screenshot()
    attach.attach_xml()

    if context == 'bstack':
        session_id = browser.driver.session_id

        with allure.step('tear down app session with id' + session_id):
            browser.quit()

        bstack = options.get_capability('bstack:options')
        attach.attach_bstack_video(session_id, bstack['userName'], bstack['accessKey'])

    browser.quit()

# def mobile_management_bstack():
#     options = UiAutomator2Options().load_capabilities({
#         # Specify device and os_version for testing
#         'platformName': 'android',
#         'platformVersion': config.android_platform_version,
#         'deviceName': config.android_device_name,
#
#         # Set URL of the application under test
#         'app': config.browserstack_app_url,
#
#         # Set other BrowserStack capabilities
#         'bstack:options': {
#             'projectName': 'First Python project',
#             'buildName': 'browserstack-build-1',
#             'sessionName': 'BStack first_test',
#
#             # Set your access credentials
#             'userName': config.USR,
#             'accessKey': config.ACCESS_KEY
#         }
#     })
#
#     with allure.step('init app session'):
#         browser.config.driver = webdriver.Remote('http://hub.browserstack.com/wd/hub', options=options)
#     browser.config.timeout = config.timeout
#     browser.config._wait_decorator = support._logging.wait_with(context=allure_commons._allure.StepContext)
#
#     yield
#
#     attach.attach_screenshot()
#     session_id = browser.driver.session_id
#
#     with allure.step('Tear down app session'):
#         browser.quit()
#
#     attach.attach_bstack_video(session_id)
