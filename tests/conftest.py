import allure
import allure_commons
import pytest
from appium import webdriver
from dotenv import load_dotenv
from selene import browser, support

from wikipedia_tests.utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        choices=['bstack', 'local_real', 'local_emulator'],
    )


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    context = request.config.getoption("--context")
    load_dotenv('.env')
    load_dotenv(dotenv_path=f'.env.{context}')
    from config import config

    options = config.to_driver_options(context)
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            config.remote_url,
            options=options
        )
    browser.config.timeout = config.timeout
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

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
