from time import sleep

from pytest_bdd import given, parsers, when

from tests.core.store import Store

store = Store()


@when(parsers.parse("check def choose_selector step {step}"))
def check_def_choose_selector(base_page, step):
    xps = base_page.xp
    texts = base_page.text
    for xp_key in xps.keys():
        locator = base_page.choose_selector(xp_key)
        # print(xp_key, locator)
        assert xps.get(xp_key) in str(locator), f"def_choose_selector wrong in xp"
        assert texts.get(xp_key) is None, f"key {xp_key} have not to in text"
    for text_key in texts.keys():
        locator = base_page.choose_selector(text_key)
        # print(text_key, locator)
        assert texts.get(text_key)[0] in str(locator), f"def_choose_selector wrong in text"
        assert xps.get(text_key) is None, f"key {text_key} have not to in xp"
    print(f"Step {step} PASS")

@when(parsers.parse("check def get_page_data step {step}"))
def check_def_get_page_data(base_page, step):
    pass
