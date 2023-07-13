from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, confloat, conint, validator

from .utils import hours_validator


class CreateOrderDto(BaseModel):
    weight: confloat(ge=0)
    regions: conint(ge=0)
    delivery_hours: list[str]
    cost: conint(ge=0)

    @validator("delivery_hours")
    def hours_validator(cls, delivery_hours):
        return hours_validator(delivery_hours)


class CreateOrderRequest(BaseModel):
    orders: list[CreateOrderDto]


class OrderDto(BaseModel):
    order_id: int
    weight: confloat(ge=0)
    regions: conint(ge=0)
    delivery_hours: list[str]
    cost: conint(ge=0)
    completed_time: Optional[datetime]

    @validator("delivery_hours")
    def hours_validator(cls, delivery_hours):
        return hours_validator(delivery_hours)


class CompleteOrder(BaseModel):
    courier_id: int
    order_id: int
    complete_time: datetime


class CompleteOrderRequestDto(BaseModel):
    complete_info: list[CompleteOrder]


class GroupOrders(BaseModel):
    group_order_id: int
    orders: list[OrderDto]


class CouriersGroupOrders(BaseModel):
    courier_id: int
    orders: list[GroupOrders]


class OrderAssignResponse(BaseModel):
    date: date
    couriers: list[CouriersGroupOrders]
