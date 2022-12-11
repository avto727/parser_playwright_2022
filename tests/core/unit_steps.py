from time import sleep

from pytest_bdd import given, parsers, when

from tests.core.store import Store

store = Store()


@when(parsers.parse("determinate total_pages to store step {step}"))
def determ_total_pages(base_page, step):
    total_pages = int(base_page.determ_last_element("paginator"))  # Сколько всего страниц
    print(f"всего страниц total_pages = {total_pages}")
    store["total_pages"] = total_pages
    print(f"Step {step} from steps.py done")
