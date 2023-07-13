from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weight = Column(Float, nullable=False)
    cost = Column(Integer, nullable=False)

    delivery_hours = relationship("DeliveryHours", backref="order", lazy="joined")
    regions = Column(
        Integer,
        ForeignKey("regions.id"),
        nullable=False,
    )
    completed_time = relationship(
        "CompletedOrder",
        backref="order",
        lazy="joined",
        uselist=False,
    )

    def to_dict(self):
        d = {
            "order_id": self.id,
            "weight": self.weight,
            "regions": self.regions,
            "delivery_hours": list(map(str, self.delivery_hours)),
            "cost": self.cost,
        }
        if self.completed_time:
            d["completed_time"] = self.completed_time.completed_time
        return d


class DeliveryHours(Base):
    __tablename__ = "delivery_hours"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)

    def __repr__(self):
        return f"{self.from_time.strftime('%H:%M')}-{self.to_time.strftime('%H:%M')}"


class CompletedOrder(Base):
    __tablename__ = "completed_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    courier_id = Column(Integer, ForeignKey("couriers.id", ondelete="CASCADE"))
    completed_time = Column(DateTime, nullable=False)

    def __repr__(self):
        return str(self.completed_time)
