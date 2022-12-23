from pytest_bdd import scenario
from tests.core.steps import *



@scenario("tester_python_web.feature", "tester_python_web")
def test_tester_python_web() -> None:
    pass


@scenario("tester_ios.feature", "tester_ios")
def test_tester_ios() -> None:
    pass


@scenario("dev_android.feature", "dev_android")
def test_dev_android() -> None:
    pass


@scenario("data_engineer.feature", "data_engineer")
def test_data_engineer() -> None:
    pass



