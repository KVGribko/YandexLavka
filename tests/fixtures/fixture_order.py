import pytest


@pytest.fixture
def order1():
    return {
        "weight": 16.7,
        "regions": 0,
        "delivery_hours": ["09:00-10:00"],
        "cost": 300,
    }


@pytest.fixture
def order2():
    return {
        "weight": 1.2,
        "regions": 5,
        "delivery_hours": ["09:00-10:00", "12:00-23:00", "23:30-23:59"],
        "cost": 100,
    }


@pytest.fixture
def order3():
    return {
        "weight": 1.2,
        "regions": 2,
        "delivery_hours": ["09:00-10:00", "12:00-23:00", "23:30-23:59"],
        "cost": 200,
    }


@pytest.fixture
def invalid_order():
    return {
        "weight": 1.2,
        "regions": None,
        "delivery_hours": ["string"],
        "cost": -200,
    }


@pytest.fixture
def orders(order1, order2, order3):
    return [order1, order2, order3]
