from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count, sum

from app.models.courier import Courier, WorkingHours
from app.models.order import CompletedOrder, Order
from app.models.region import Region
from app.shemas.courier import CourierDto, CreateCourierDto, GetCourierMetaInfoResponse

from .base import BaseRepository


class CouriersRepository(BaseRepository):
    def create_couriers(
        self, db: Session, couriers: list[CreateCourierDto]
    ) -> list[CourierDto]:
        new_couriers = []
        for courier in couriers:
            regions = self.__get_regions(db, courier.regions)
            working_hours = self._get_working_hours(courier.working_hours, WorkingHours)
            new_courier = Courier(
                courier_type=courier.courier_type,
                regions=regions,
                working_hours=working_hours,
            )
            new_couriers.append(new_courier)
            db.add(new_courier)
        db.commit()
        return [CourierDto.parse_obj(courier.to_dict()) for courier in new_couriers]

    def get_meta_info(
        self,
        db: Session,
        courier_id: int,
        start_date: date,
        end_date: date,
    ) -> GetCourierMetaInfoResponse:
        query = (
            db.query(
                Courier,
                sum(Order.cost).label("sum"),
                count(Order.cost).label("count"),
            )
            .filter(
                CompletedOrder.courier_id == courier_id,
                CompletedOrder.completed_time.between(start_date, end_date),
            )
            .join(CompletedOrder, CompletedOrder.courier_id == Courier.id)
            .join(Order, Order.id == CompletedOrder.order_id)
            .group_by(Courier.id)
        )
        courier, cost_sum, order_count = db.execute(query).one()
        meta_info = courier.to_dict()

        if order_count != 0:
            earnings_coeff = courier.courier_type.get_coeff_for_earnings()
            earnings = self.__get_earnings(cost_sum, earnings_coeff)
            meta_info["earnings"] = earnings

            rating_coeff = courier.courier_type.get_coeff_for_rating()
            rating = self.__get_rating(start_date, end_date, rating_coeff, order_count)
            meta_info["rating"] = rating
        return GetCourierMetaInfoResponse.parse_obj(meta_info)

    def __get_regions(self, db, regions):
        return [self.get_or_create(db, Region, id=region) for region in regions]

    @staticmethod
    def __get_rating(start_date, end_date, coeff, order_count):
        SECONDS_IN_HOUR = 3600
        HOURS_IN_DAY = 24
        duration = end_date - start_date
        days, seconds = duration.days, duration.seconds
        hours = days * HOURS_IN_DAY + (seconds / SECONDS_IN_HOUR)
        return None if hours == 0 else coeff * (order_count / hours)

    @staticmethod
    def __get_earnings(cost_sum, coeff):
        return cost_sum * coeff


couriers = CouriersRepository(Courier)
