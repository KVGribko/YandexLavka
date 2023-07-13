import pytest
from fastapi import status
from fastapi.testclient import TestClient

from datetime import datetime
from app.shemas.order import OrderDto


def test_create_orders(client: TestClient, orders):
    data = {"orders": orders}
    response = client.post("/orders", json=data)
    assert response.status_code == status.HTTP_200_OK
    [OrderDto(**order) for order in response.json()]

    response_json = response.json()
    assert len(response_json) == len(data["orders"])

    for i, new_order in enumerate(response_json):
        del new_order["order_id"]
        del new_order["completed_time"]
        old_order = data["orders"][i]
        assert new_order == old_order, f"{new_order} != {old_order}"


def test_create_invalid_order(client: TestClient, invalid_order):
    data = {"orders": [invalid_order]}
    response = client.post("/couriers", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_orders(client: TestClient, orders):
    response = client.get("/orders", params={"limit": len(orders) + 1})
    assert response.status_code == status.HTTP_200_OK
    [OrderDto(**order) for order in response.json()]

    response_json = response.json()
    assert len(response_json) == len(orders)

    for i, new_order in enumerate(response_json):
        del new_order["order_id"]
        del new_order["completed_time"]
        old_order = orders[i]
        assert new_order == old_order, f"{new_order} != {old_order}"


def test_get_order_by_id(client: TestClient):
    response = client.get("/orders")
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    order = response_json[0]
    del order["completed_time"]
    order_id = order["order_id"]

    response = client.get(f"/orders/{order_id}/")
    assert response.status_code == status.HTTP_200_OK
    OrderDto(**response.json())
    assert order == response.json()


@pytest.mark.dependency(depends=["test_create_orders", "test_create_couriers"])
def test_create_completed_order(client: TestClient, couriers, orders):
    response = client.get("/couriers", params={"limit": len(couriers) + 1})
    response_json = response.json()["couriers"]
    couriers_id = [courier["courier_id"] for courier in response_json]

    response = client.get("/orders", params={"limit": len(orders) + 1})
    order_id = [order["order_id"] for order in response.json()]

    comlete_orders = []
    for id in order_id:
        co = {
            "courier_id": couriers_id[0],
            "order_id": id,
            "complete_time": str(datetime.now()),
        }
        comlete_orders.append(co)

    data = {"complete_info": comlete_orders}
    response = client.post("/orders/complete/", json=data)
    assert response.status_code == status.HTTP_200_OK
    [OrderDto(**order) for order in response.json()]
