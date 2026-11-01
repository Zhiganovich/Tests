from ui.steps.catalog_steps import CatalogSteps

def test_count_catalog(page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login("standard_user", "secret_sauce")
    assert catalog_steps.get_products_count() == 6

def test_sorted_by_name(page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login("standard_user", "secret_sauce")

    catalog_steps.sort_items("az")
    assert catalog_steps.get_product_names() == sorted(catalog_steps.get_product_names())

    catalog_steps.sort_items("za")
    assert catalog_steps.get_product_names() == sorted(catalog_steps.get_product_names(), reverse=True)

def test_sort_by_price(page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login("standard_user", "secret_sauce")

    catalog_steps.sort_items("lohi")
    assert catalog_steps.get_product_prices() == sorted(catalog_steps.get_product_prices())

    catalog_steps.sort_items("hilo")
    assert catalog_steps.get_product_prices() == sorted(catalog_steps.get_product_prices(), reverse=True)

def test_add_to_cart(page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login("standard_user", "secret_sauce")

    catalog_steps.add_to_cart("Sauce Labs Bike Light")
    assert catalog_steps.get_cart_count() == 1

def test_add_and_remove_onesie(page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login("standard_user", "secret_sauce")

    catalog_steps.add_to_cart("Sauce Labs Onesie")
    assert catalog_steps.get_cart_count() == 1

    catalog_steps.remove_from_cart("Sauce Labs Onesie")
    assert catalog_steps.get_cart_count() == 0

def test_product_details_onesie(page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = catalog_steps.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price

def test_product_details_fleece_jacket(page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = catalog_steps.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name
    assert price == detail_price

def test_remove_item_from_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.remove_from_cart("Test.allTheThings() T-Shirt (Red)")