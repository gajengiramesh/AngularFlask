import logging

from flask import Flask, request, g
from flask_compress import Compress

from db.services.context import db_session
from end_points.authentication import auth_service
from end_points.rest_utils import response
from end_points.user import user_service
from exceptions import AppException
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
# Compress(app)
app.config['SECRET_KEY'] = 'TesTing123987546'
logger = logging.getLogger(__name__)

#
# class MyResponse(Response):
#     @classmethod
#     def force_type(cls, rv, environ=None):
#         print('ramesh')
#         if isinstance(rv, dict) or isinstance(rv,int):
#             rv = jsonify(rv)
#             return rv
#         return super(Response, cls).force_type(rv, environ)
#
# app.response_class = MyResponse
app.register_blueprint(auth_service)
app.register_blueprint(user_service)
compress = Compress()
compress.init_app(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@app.errorhandler(Exception)
def handle_bad_request(e):
    if isinstance(e, AppException):
        logger.debug(str(e))
        return response(resp=str(e), http_status=e.http_status_code)
    else:
        logger.exception(e)
        return response(str(e), http_status=500)


@app.before_request
def before_request():
    if not 'auth' in request.url:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        g.user = current_user
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())


# @app.route("/")
# def hello():
#     return "Hello World!"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    from db.services.context import init_db

    init_db()
    app.run()
