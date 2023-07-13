from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    couriers = relationship(
        "Courier", secondary="courier_region", back_populates="regions", lazy="joined"
    )
    orders = relationship("Order", lazy="joined")

    def __repr__(self):
        return str(self.id)
