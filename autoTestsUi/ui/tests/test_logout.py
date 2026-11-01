from ui.pages.login_page import LoginPage
from ui.pages.catalog_page import CatalogPage
from playwright.sync_api import expect

def test_logout(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0

    catalog_page.logout()

    expect(page).to_have_url(LoginPage.URL)


def test_logout_visual_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("visual_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0

    catalog_page.logout()

    expect(page).to_have_url(LoginPage.URL)
