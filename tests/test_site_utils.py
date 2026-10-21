import site

from site_utils import (
    get_site_packages,
    get_user_base,
    get_user_site_packages,
    is_user_site_enabled,
)


def test_get_site_packages():
    assert get_site_packages() == list(site.getsitepackages())


def test_get_user_base():
    assert get_user_base() == site.getuserbase()


def test_get_user_site_packages():
    assert get_user_site_packages() == site.getusersitepackages()


def test_is_user_site_enabled():
    assert is_user_site_enabled() == bool(site.ENABLE_USER_SITE)
