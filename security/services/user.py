
from flask import Blueprint
user_service = Blueprint('user_service',__name__)
from  db.services.context import db_session
from security.models.user import User ,returns_user

@user_service.route("/user/by_id/<user_id>")
def user_by_id(user_id):
    u = User.query.filter(User.id == user_id).first()
    return {'name':'Ramesh','id':1}
    #return u

@user_service.route("/user/by_name/<user_name>")
@returns_user
def user_by_name(user_name):
    u = User.query.filter(User.name == user_name).first()
    print(u)
    return u


@user_service.route("/user/add/<user_name>/<email>")
def add_user(user_name,email):
    u = User(user_name, email)
    db_session.add(u)
    db_session.commit()
    return  u.id