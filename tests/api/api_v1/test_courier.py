import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.shemas.courier import CourierDto, CreateCouriersResponse, GetCouriersResponse


def test_create_couriers(client: TestClient, couriers):
    data = {"couriers": couriers}
    response = client.post("/couriers", json=data)
    assert response.status_code == status.HTTP_200_OK
    CreateCouriersResponse(**response.json())

    response_json = response.json()["couriers"]
    assert len(response_json) == len(data["couriers"])

    for i, new_courier in enumerate(response_json):
        del new_courier["courier_id"]
        old_courier = data["couriers"][i]
        assert new_courier == old_courier, f"{new_courier} != {old_courier}"


def test_create_invalid_couriers(client: TestClient, invalid_courier):
    data = {"couriers": [invalid_courier]}
    response = client.post("/couriers", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.dependency(depends=["test_create_couriers"])
def test_get_couriers(client: TestClient, couriers):
    response = client.get("/couriers", params={"limit": len(couriers) + 1})
    assert response.status_code == status.HTTP_200_OK
    GetCouriersResponse(**response.json())

    response_json = response.json()["couriers"]
    assert len(response_json) == len(couriers)

    for i, new_courier in enumerate(response_json):
        del new_courier["courier_id"]
        old_courier = couriers[i]
        assert new_courier == old_courier, f"{new_courier} != {old_courier}"


@pytest.mark.dependency(depends=["test_create_couriers"])
def test_get_courier_by_id(client: TestClient):
    response = client.get("/couriers")
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()["couriers"]
    courier = response_json[0]
    courier_id = courier["courier_id"]

    response = client.get(f"/couriers/{courier_id}/")
    assert response.status_code == status.HTTP_200_OK
    CourierDto(**response.json())
    assert courier == response.json()
