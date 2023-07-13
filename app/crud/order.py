from sqlalchemy.orm import Session

from app.models.courier import Courier
from app.models.order import CompletedOrder, DeliveryHours, Order
from app.models.region import Region
from app.shemas.order import CompleteOrder, CreateOrderDto, OrderDto

from .base import BaseRepository
from .exception import CourierNotExists, OrderAlreadyCompleted, OrderNotExists


class OrdersRepository(BaseRepository):
    def create_orders(
        self, db: Session, orders: list[CreateOrderDto]
    ) -> list[OrderDto]:
        new_orders = []
        for order in orders:
            regions = self.get_or_create(db, Region, id=order.regions)
            delivery_hours = self._get_working_hours(
                order.delivery_hours, DeliveryHours
            )
            new_order = Order(
                weight=order.weight,
                cost=order.cost,
                regions=regions.id,
                delivery_hours=delivery_hours,
            )
            new_orders.append(new_order)
            db.add(new_order)
        db.commit()
        return [OrderDto.parse_obj(order.to_dict()) for order in new_orders]

    def create_completed_orders(
        self,
        db: Session,
        completed_orders: list[CompleteOrder],
    ) -> list[OrderDto]:
        new_completed_orders = []
        for order in completed_orders:
            self.__check_new_completed_order(db, order)
            new_order = CompletedOrder(
                order_id=order.order_id,
                courier_id=order.courier_id,
                completed_time=order.complete_time,
            )
            db.add(new_order)
            new_completed_orders.append(new_order)
        db.commit()
        return [
            OrderDto.parse_obj(completed_order.order.to_dict())
            for completed_order in new_completed_orders
        ]

    def __check_new_completed_order(self, db: Session, order: CompleteOrder):
        if self.__is_not_exists_by_id(db, Courier, order.courier_id):
            raise CourierNotExists(f"Courier with id={order.courier_id} does not exist")
        if self.__is_not_exists_by_id(db, Order, order.order_id):
            raise OrderNotExists(f"Order with id={order.order_id} does not exist")
        if self.__is_alredy_completed(db, order.order_id):
            raise OrderAlreadyCompleted(
                f"Order with id={order.order_id} already completed"
            )

    def __is_not_exists_by_id(self, db: Session, model, id: int):
        obj = db.query(model).filter(model.id == id).one_or_none()
        return obj is None

    def __is_alredy_completed(self, db: Session, order_id):
        q = db.query(CompletedOrder).filter(CompletedOrder.order_id == order_id)
        return bool(db.query(CompletedOrder.order_id).filter(q.exists()).scalar())


orders = OrdersRepository(Order)
