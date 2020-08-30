import marshmallow
from datetime import datetime
from marshmallow import validates, ValidationError, validates_schema

from app.api.schemas.customer import CustomerSchema
from app.extensions import ma, db
from app.models import Customer
from app.models.reservation import Reservation


class ReservationSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    timestamp = ma.DateTime(dump_only=True)
    confirmed = ma.Boolean(dump_only=True)

    start = ma.Date(required=True)
    end = ma.Date(required=True)
    customer_id = ma.Int(load_only=True, required=True)

    customer = ma.Pluck(CustomerSchema, 'id', many=False)

    class Meta:
        model = Reservation
        sqla_session = db.session
        load_instance = True

    @validates("customer_id")
    def validate_customer_id(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            raise ValidationError("Customer with id: #%d does not exist." % customer_id)

    @validates_schema(skip_on_field_errors=True)
    def validate_date(self, data, **kwargs):
        if not data['start'] <= data['end']:
            raise marshmallow.ValidationError(
                'start should not be less than end',
                'start'
            )

        if data['start'] < datetime.today().date():
            raise marshmallow.ValidationError(
                'start can not be in the past',
                'start'
            )


        if not Reservation.is_free(data['start'], data['end']):
            raise marshmallow.ValidationError(
                'there is already an existing reservation',
                'start'
            )
