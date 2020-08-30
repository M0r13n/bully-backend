from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.api.schemas import CustomerSchema
from app.extensions import db


class CustomerList(Resource):

    def post(self):
        schema = CustomerSchema()

        try:
            customer = schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        db.session.add(customer)
        db.session.commit()

        return {"msg": "customer created", "customer": schema.dump(customer)}, 201
