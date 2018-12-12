
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def hello1():
    print('hello1')
    return "Hello World 11111111111111!"


if __name__ == '__main__':
    app.run()