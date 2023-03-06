from flask import Flask, request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

from db import User, Session
from schema import validate_create_user
from errors import HttpError
from advertisements import AdvertisementView


app = Flask('app')
bcrypt = Bcrypt(app)


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({
        'status': 'error',
        'description': error.massage
    })
    http_response.status_code = error.status_code
    return http_response


def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    else:
        return user


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'username': user.username,
                'creation_time': user.creation_time.isoformat()
            })

    def post(self):
        json_data = validate_create_user(request.json)
        password = json_data['password']
        password = password.encode()
        password = bcrypt.generate_password_hash(password)
        password = password.decode()
        json_data['password'] = password

        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'user already exists')
            return jsonify({
                'id': new_user.id,
                'creation_time': new_user.creation_time
            })

    def patch(self, user_id: int):
        json_data = request.json
        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
            return jsonify({
                'status': 'success'
            })

    def delete(self, user_id: int):
        with Session as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
        return jsonify({
            'status': 'success'
        })


app.add_url_rule(
    '/users/<int:user_id>',
    view_func=UserView.as_view('user_details'),
    methods=['GET', 'PATCH', 'DELETE']
)
app.add_url_rule(
    '/users',
    view_func=UserView.as_view('users'),
    methods=['POST']
)
app.add_url_rule(
    '/users/<int:user_id>/adv/<int:adv_id>',
    view_func=AdvertisementView.as_view('adv_details'),
    methods=['GET', 'PATCH', 'DELETE']
)
app.add_url_rule(
    '/users/<int:user_id>/adv',
    view_func=AdvertisementView.as_view('advertisement'),
    methods=['POST']
)

app.run(host='localhost', port=5000)
