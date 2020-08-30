from datetime import datetime

from sqlalchemy.orm import relationship

from app.extensions import db


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False, unique=False, index=True)
    last_name = db.Column(db.String(255), nullable=False, unique=False, index=True)
    street = db.Column(db.String(255), nullable=False, unique=False, index=True)
    zip_code = db.Column(db.String(10), nullable=False, unique=False, index=True)
    city = db.Column(db.String(255), nullable=False, unique=False, index=True)
    tel = db.Column(db.String(64), nullable=True, unique=False, index=True)
    email = db.Column(db.String(255), nullable=False, unique=False, index=True)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

    reservations = relationship("Reservation", back_populates="customer")
