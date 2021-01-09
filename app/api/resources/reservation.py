from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.api.schemas import ReservationSchema
from app.common.dates import first_day_of_current_month, first_day_of_next_month
from app.common.pagination import paginate
from app.common.slack import send_notification
from app.extensions import db
from app.models.reservation import Reservation


class ReservationResource(Resource):

    def get(self, reservation_id):
        schema = ReservationSchema()
        reservation = Reservation.query.get_or_404(reservation_id)
        return {"reservation": schema.dump(reservation)}


class ReservationList(Resource):

    def get(self):
        schema = ReservationSchema(many=True)
        start = request.args.get('start', first_day_of_current_month())
        end = request.args.get('end', first_day_of_next_month())
        query = Reservation.query.filter(
            start <= Reservation.end,
            end >= Reservation.start
        )
        return paginate(query, schema)

    def post(self):
        schema = ReservationSchema()
        try:
            reservation = schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        db.session.add(reservation)
        db.session.commit()

        send_notification(
            f"{reservation.customer.first_name} {reservation.customer.last_name} hat eine Reservierung erstellt."
        )

        return {"msg": "reservation created", "reservation": schema.dump(reservation)}, 201
