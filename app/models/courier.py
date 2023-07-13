from sqlalchemy import Column, Enum, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.shemas.courier import CourierType


class CourierRegion(Base):
    __tablename__ = "courier_region"

    courier_id = Column(Integer, ForeignKey("couriers.id", ondelete="CASCADE"),  primary_key=True)
    region_id = Column(Integer, ForeignKey("regions.id", ondelete="CASCADE"), primary_key=True)


class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    courier_type = Column(Enum(CourierType), default=CourierType.FOOT)

    working_hours = relationship("WorkingHours", lazy="joined")
    regions = relationship("Region", secondary="courier_region", back_populates="couriers", lazy="joined")
    completed_orders = relationship("CompletedOrder", backref="courier", lazy="joined")

    def to_dict(self):
        return {
            "courier_id": int(self.id),
            "courier_type": self.courier_type.value,
            "regions": sorted([region.id for region in self.regions]),
            "working_hours": list(map(str, self.working_hours)),
        }


class WorkingHours(Base):
    __tablename__ = "working_hours"

    id = Column(Integer, primary_key=True, autoincrement=True)
    courier_id = Column(Integer, ForeignKey("couriers.id", ondelete="CASCADE"))
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)

    def __repr__(self):
        return f"{self.from_time.strftime('%H:%M')}-{self.to_time.strftime('%H:%M')}"
