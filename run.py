from flask import Flask ,Response , jsonify
from  db.services.context import db_session
from security.services.authentication  import auth_service
from security.services.user import user_service
from flask_cors import CORS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TesTing123987546'
CORS(app)

class MyResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        print('ramesh')
        if isinstance(rv, dict) or isinstance(rv,int):
            rv = jsonify(rv)
            return rv
        return super(Response, cls).force_type(rv, environ)

app.response_class = MyResponse
app.register_blueprint(auth_service)
app.register_blueprint(user_service)

@app.errorhandler(Exception)
def handle_bad_request(e):
    return str(e), 500

@app.route("/")
def hello():
    return "Hello World!"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    from db.services.context import init_db
    from security.models.user import User
    init_db()
    app.run()