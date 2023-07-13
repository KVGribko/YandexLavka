import pytest


@pytest.fixture
def courier1():
    return {
        "courier_type": "FOOT",
        "regions": [0],
        "working_hours": ["09:00-12:00"],
    }


@pytest.fixture
def courier2():
    return {
        "courier_type": "BIKE",
        "regions": [0, 2, 5],
        "working_hours": ["09:00-10:00", "12:00-23:00", "23:30-23:59"],
    }


@pytest.fixture
def courier3():
    return {
        "courier_type": "AUTO",
        "regions": [3],
        "working_hours": ["12:00-23:00"],
    }


@pytest.fixture
def invalid_courier():
    return {
        "courier_type": "AUTO",
        "regions": [3],
        "working_hours": ["59:00-23:00", "string"],
    }


@pytest.fixture
def couriers(courier1, courier2, courier3):
    return [courier1, courier2, courier3]
