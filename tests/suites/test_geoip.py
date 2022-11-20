from pytest_bdd import scenario


@scenario("api/geoip/geoip.feature", "version_geoip")
def test_get_version_geoip() -> None:
    pass


@scenario("api/geoip/geoip.feature", "status_geoip")
def test_get_status_geoip() -> None:
    pass
