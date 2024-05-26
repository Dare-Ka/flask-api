import flask
from flask import request
from sqlalchemy.exc import IntegrityError

from app import app
from error_handler import HttpError
from models import Advertisement, User, Session


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
