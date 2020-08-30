from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import relationship

from app.extensions import db


class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

    start = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)

    confirmed = db.Column(db.Boolean, default=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer", back_populates="reservations")

    @classmethod
    def is_free(cls, start: datetime, end: datetime) -> bool:
        # (StartA <= EndB) and (EndA >= StartB)
        overlapping = cls.query.filter(
            and_(
                start <= cls.end,
                end >= cls.start
            )
        ).first()
        return overlapping is None
