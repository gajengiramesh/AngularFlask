from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from db.services.context import db_session
from end_points.rest_utils import response, get_current_user
from schemas.security.user import UserSchema
from services.security.users import UserService

user_service = Blueprint('user_service', __name__)


def _get_service():
    return UserService(session=db_session,request_user=get_current_user())

@user_service.route("/users/<user_id>", methods=['GET'])
@user_service.route("/users", methods=['GET'])
@jwt_required()
def get_users(user_id=None):

    # UserService(db_session=db_session,request_user=request.g.user)
    if user_id:
        user_id = int(user_id)
    users = _get_service().get_objects_dump(obj_id=user_id)
    resp = UserSchema().dump(users, many=True)
    resp = response(resp)
    return resp


@user_service.route("/users", methods=['POST'])
def add_user():
    data = UserSchema().loads(request.data)
    users = UserService(session=db_session, request_user=None).add_user(data=data)
    resp = UserSchema().dump(users, many=True)
    resp = response(resp)
    return resp
    # return u

# @user_service.route("/user/by_name/<user_name>")
# @returns_user
# def user_by_name(user_name):
#     u = User.query.filter(User.name == user_name).first()
#     print(u)
#     return u
#
#
# @user_service.route("/user/add/<user_name>/<email>")
# def add_user(user_name,email):
#     u = User(user_name, email)
#     db_session.add(u)
#     db_session.commit()
#     return  u.id
