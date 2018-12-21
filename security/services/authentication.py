
from flask import Blueprint,request
auth_service = Blueprint('auth_service',__name__)
from  db.services.context import db_session
from security.models.user import User
import json
from flask import current_app as app
from Crypto.Cipher import AES
import base64

@auth_service.route("/auth/login/",methods=['POST'])
def login():
    dataDict = json.loads(request.data)
    user_name = dataDict['user_name']
    password = dataDict['password']
    u = User.query.filter(User.login == user_name).first()

    if not u:
        raise Exception('Authentication failed')
    else:
        if u.password == password:
            secret_key = app.config['SECRET_KEY']
            cipher = AES.new(secret_key, AES.MODE_ECB)
            encoded = base64.b64encode(cipher.encrypt((str(u.id) + '_'+ u.name).rjust(32))).decode("utf-8")
            return {'user_id':u.id,'token':encoded}
        # u = User('admin', 'admin@localhost')
        # db_session.add(u)
        # db_session.commit()
        else:
            raise Exception('Authentication failed')

@auth_service.route("/auth/users")
def get_users():
    User.query.all()
    return User.query.all()