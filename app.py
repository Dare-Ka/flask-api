from typing import Type

import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Advertisement, Session
from schema import CreateAd, UpdateAd

app = Flask('app')

def validate_json(json_data: dict, schema_class: Type[CreateAd] | Type[UpdateAd]):
    try:
        return schema_class(**json_data).dict(exlude_unset=True)
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


def add_ad(ad: Advertisement):     #Переписать с использованием User!!!!!
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "advertisement already exists")

class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code


class AdView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)

    def post(self):
        ad_data = validate_json(request.json, CreateAd)
        ad = Advertisement(**ad_data)
        add_ad(ad)
        return jsonify(ad.dict)

    def patch(self, ad_id: int):
        ad_data = validate_json(request.json, UpdateAd)
        ad = get_ad_by_id(ad_id)
        for field, value in ad_data.items():
            setattr(ad, field, value)
        add_ad(ad)
        return jsonify(ad.dict)

    def delete(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"status": "deleted"})


ad_view = AdView.as_view('advertisements')


app.add_url_rule('/ad/<int:ad_id>', view_func=ad_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ad', view_func=ad_view, methods=['POST'])

if __name__ == '__main__':
    app.run()