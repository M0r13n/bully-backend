from marshmallow.validate import Length

from app.extensions import ma, db
from app.models.customer import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    registered_on = ma.DateTime(dump_only=True)

    first_name = ma.String(required=True, validate=Length(1, 255))
    last_name = ma.String(required=True, validate=Length(1, 255))
    street = ma.String(required=True, validate=Length(1, 255))
    zip_code = ma.String(required=True, validate=Length(1, 10))
    city = ma.String(required=True, validate=Length(1, 255))
    tel = ma.String(required=False, allow_none=True, validate=Length(max=64))
    email = ma.Email(required=True, validate=Length(1, 255))

    class Meta:
        model = Customer
        sqla_session = db.session
        load_instance = True
