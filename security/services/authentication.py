
from flask import Blueprint
auth_service = Blueprint('auth_service',__name__)
from  db.services.context import db_session
from security.models.user import User

@auth_service.route("/auth/login/<user_name>/<password>")
def login(user_name,password):
    u = User.query.filter(User.name == 'admin').first()
    if not u:
        u = User('admin', 'admin@localhost')
        db_session.add(u)
        db_session.commit()

        return 'true'
    else:
        return 'false'

@auth_service.route("/auth/users")
def get_users():
    User.query.all()
    return User.query.all()