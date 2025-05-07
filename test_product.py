import pytest
from products import Product, NonStockedProduct

def test_product_init():
    p = Product("Test", price=100, quantity=10)
    assert p.name == "Test"
    assert p.price == 100
    assert p.quantity == 10

def test_invalid_product_name():
    with pytest.raises(ValueError):
        Product("", price=100, quantity=10)

def test_negative_price():
    with pytest.raises(ValueError):
        Product("Test", price=-100, quantity=10)

def test_negative_quantity():
    with pytest.raises(ValueError):
        Product("Test", price=100, quantity=-10)

def test_product_becomes_inactive_at_zero_quantity():
    p = Product("Test", price=100, quantity=1)
    p.buy(1)
    assert not p.is_active()

def test_purchase_updates_quantity():
    p = Product("Test", price=100, quantity=2)
    res = p.buy(1)
    assert res == 100
    assert p.quantity == 1

def test_buy_too_much():
    p = Product("Test", price=100, quantity=10)
    with pytest.raises(ValueError):
        p.buy(11)

