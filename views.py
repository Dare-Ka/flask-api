from flask import jsonify, request
from flask.views import MethodView

from app import get_user_by_id, validate_json, add_user, get_ad_by_id, add_ad
from models import User, Advertisement
from schema import CreateUser, UpdateUser, CreateAd, UpdateAd


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