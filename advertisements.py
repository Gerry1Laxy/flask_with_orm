from flask.views import MethodView
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from db import Advertisement, Session
from errors import HttpError
from schema import validate_create_adv, validate_update_adv


class AdvertisementView(MethodView):

    def get(self, user_id: int, adv_id: int):
        adv = self.get_adv(adv_id)
        return jsonify({
            'id': adv.id,
            'title': adv.title,
            'description': adv.description,
            'created_at': adv.created_at,
            'user_id': adv.user_id
        })

    def post(self, user_id: int):
        json_data = validate_create_adv(request.json)
        json_data['user_id'] = user_id
        with Session() as session:
            adv = Advertisement(**json_data)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'advertisement already exists')
            return jsonify({
                'id': adv.id,
            })

    def patch(self, user_id: int, adv_id: int):
        json_data = validate_update_adv.validate(request.json)
        with Session() as session:
            adv = self.get_adv(adv_id)
            for field, value in json_data.items():
                if value:
                    setattr(adv, field, value)
            session.add(adv)
            session.commit()
        return jsonify({
            'status': 'success'
        })

    def delete(self, user_id: int, adv_id: int):
        with Session() as session:
            adv = self.get_adv(adv_id)
            session.delete(adv)
            session.commit()
        return jsonify({
            'status': 'success'
        })

    def get_adv(self, adv_id: int):
        adv = Advertisement.query.get(adv_id)
        if adv is None:
            raise HttpError(404, 'advertisement not found')
        else:
            return adv
