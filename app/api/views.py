import logging

from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from app.api.resources.customer import CustomerList
from app.api.resources.reservation import ReservationResource, ReservationList

logger = logging.getLogger(__name__)
blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

# Reservations
api.add_resource(ReservationResource, "/reservation/<int:reservation>", endpoint="reservation_by_id")
api.add_resource(ReservationList, "/reservation", endpoint="reservations")

# Customer
api.add_resource(CustomerList, "/customer", endpoint="customers")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    logging.error(e)
    return jsonify(e.messages), 400
