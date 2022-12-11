from time import sleep

from pytest_bdd import given, parsers, when

from tests.core.store import Store

store = Store()


@when(parsers.parse("check def choose_selector step {step}"))
def check_def_choose_selector(base_page, step):
    xps = base_page.xp
    for xp in xps.keys():
        locator = base_page.choose_selector(xp)
        print(xp, locator)
    texts = base_page.text
    for text in texts.keys():
        locator = base_page.choose_selector(text)
        print(text, locator)
