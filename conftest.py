import configparser
import os
import pytest

from tests.core.api import API
from tests.core.store import Store
from utils.app_config import AppConfig
from tests.core.base_plw import BasePage
from playwright.sync_api import Playwright

os_name = os.name
match os_name:
    case "posix":
        chrome = "chromedriver"
    case "nt":
        chrome = "chromedriver.exe"
    case "unix":
        chrome = "chromedriver"

store = Store()


def pytest_addoption(parser):
    parser.addoption(
        "--cfg",
        action="store",
        default="",
        help="Choice config from config directory",
    )


@pytest.fixture
def client():
    yield API()


@pytest.fixture
def base_page(setup_browser):
    yield BasePage(setup_browser)


class Device:
    def __init__(self, config, browser_name, playwright: Playwright):
        self.browser_name = browser_name
        self.config = config
        self.path_project = os.getcwd()
        self.user_profile_dir = f"{config['MAIN']['user_profile_dir']}"
        browser, context, page = self.web_full_version(browser_name, playwright)
        self.browser = browser
        self.context = context
        self.page = page

    @staticmethod
    def web_full_version(browser_name, playwright: Playwright):
        browser = None
        context = None
        page = None
        if browser_name == "firefox":
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
        elif browser_name == "chromium":
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
        elif browser_name == "chrome":
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
        return browser, context, page

    def __repr__(self):
        sett = (self.browser, self.context, self.page)
        return sett


@pytest.fixture(scope="session")
def setup_browser(request, config, playwright: Playwright):
    browser_name = config["MAIN"]["browser_name"]
    sett = Device(config, browser_name, playwright)
    yield sett
    print("\nquit browser..")
    sett.context.close()
    sett.browser.close()


@pytest.fixture(scope="session")
def config(request):
    config_name = request.config.getoption("--cfg")
    if config_name != "":
        config = configparser.ConfigParser()
        config.read(config_name)
    else:
        config = AppConfig().get_config()
    return config