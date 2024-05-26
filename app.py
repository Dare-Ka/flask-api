from typing import Type

import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Advertisement, User, Session
from schema import CreateAd, UpdateAd, CreateUser, UpdateUser

app = Flask('app')


def validate_json(json_data: dict, schema_class: Type[CreateAd] | Type[UpdateAd] | Type[CreateUser] | Type[UpdateUser]):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


def get_ad_by_id(ad_id: int):
    ad = request.session.query(Advertisement).get(ad_id)
    if ad is None:
        raise HttpError(404, "advertisement not found")
    return ad


def get_user_by_id(user_id: int):
    user = request.session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def add_ad(ad: Advertisement, user: User):
    ad.owner = user
    request.session.add(ad)
    request.session.commit()


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "user already exists")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = validate_json(request.json, CreateUser)
        user = User(**user_data)
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id: int):
        user_data = validate_json(request.json, UpdateUser)
        user = get_user_by_id(user_id)
        for field, value in user_data.items():
            setattr(user, field, value)
        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "deleted"})


class AdView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)

    def post(self, user_id: int):
        ad_data = validate_json(request.json, CreateAd)
        ad = Advertisement(**ad_data)
        user = get_user_by_id(user_id)
        add_ad(ad, user)
        return jsonify(ad.dict)

    def patch(self, ad_id: int, user_id: int):
        ad_data = validate_json(request.json, UpdateAd)
        ad = get_ad_by_id(ad_id)
        for field, value in ad_data.items():
            setattr(ad, field, value)
        add_ad(ad, User.id)
        return jsonify(ad.dict)

    def delete(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"status": "deleted"})


ad_view = AdView.as_view('advertisements')
user_view = UserView.as_view('users')


app.add_url_rule('/ad/show/<int:ad_id>', view_func=ad_view, methods=['GET'])
app.add_url_rule('/ad/<int:ad_id>', view_func=ad_view, methods=['DELETE'])
app.add_url_rule('/user/<int:user_id>/ad/<int:ad_id>', view_func=ad_view, methods=['PATCH'])
app.add_url_rule('/user/<int:user_id>/ad', view_func=ad_view, methods=['POST'])

app.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/user', view_func=user_view, methods=['POST'])

if __name__ == '__main__':
    app.run()
