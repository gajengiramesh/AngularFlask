import logging

from flask import Blueprint, request

from db.services.context import db_session
from end_points.rest_utils import response
from schemas.security.user import UserSchema
from services.security.auth import Authenticator
from flask_jwt_extended import create_access_token

auth_service = Blueprint('auth_service', __name__)
from models.security.user import User
import json

# from Crypto.Cipher import AES
logger = logging.getLogger(__name__)


@auth_service.route("/auth/login", methods=['POST'])
def login():
    dataDict = json.loads(request.data)
    login_id = dataDict['login_id']
    password = dataDict['password']
    user = Authenticator(session=db_session).authenticate(login_id=login_id, password=password)
    if not user:
        raise Exception("Error in Authenticator")
    else:
        access_token = create_access_token(identity=login_id)
        resp = UserSchema().dump(user)
        resp['access_token']  = access_token
        resp = response(resp)
        return resp
    # secret_key = app.config['SECRET_KEY']
    #         # cipher = AES.new(secret_key, AES.MODE_ECB)
    #         # encoded = base64.b64encode(cipher.encrypt((str(u.id) + '_'+ u.name).rjust(32))).decode("utf-8")
    #         encoded = ''
    #         return {'user_id':u.id,'token':encoded}
    # u = User('admin', 'admin@localhost')
    # db_session.add(u)
    # db_session.commit()


@auth_service.route("/auth/users")
def get_users():
    User.query.all()
    return User.query.all()
