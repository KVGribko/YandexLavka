from enum import Enum
from typing import Optional

from pydantic import BaseModel, conint, validator

from .utils import hours_validator


class CourierType(str, Enum):
    FOOT = "FOOT"
    BIKE = "BIKE"
    AUTO = "AUTO"

    def get_coeff_for_earnings(self):
        if self == self.FOOT:
            return 2
        if self == self.BIKE:
            return 3
        if self == self.AUTO:
            return 4

    def get_coeff_for_rating(self):
        if self == self.FOOT:
            return 3
        if self == self.BIKE:
            return 2
        if self == self.AUTO:
            return 1


class CreateCourierDto(BaseModel):
    courier_type: CourierType
    regions: list[conint(ge=0)]
    working_hours: list[str]

    @validator("working_hours")
    def hours_validator(cls, working_hours):
        return hours_validator(working_hours)


class CreateCourierRequest(BaseModel):
    couriers: list[CreateCourierDto]


class CourierDto(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: list[conint(ge=0)]
    working_hours: list[str]

    @validator("working_hours")
    def hours_validator(cls, working_hours):
        return hours_validator(working_hours)


class CreateCouriersResponse(BaseModel):
    couriers: list[CourierDto]


class GetCouriersResponse(CreateCouriersResponse):
    limit: int
    offset: int


class GetCourierMetaInfoResponse(CourierDto):
    rating: Optional[int]
    earnings: Optional[int]
