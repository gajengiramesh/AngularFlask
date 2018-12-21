from sqlalchemy import Column, Integer, String
from db.services.context import Base
from flask import Flask ,Response
from functools import wraps

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    password = Column(String(50))
    name = Column(String(50) )
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)




def returns_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        r = {'login':r.login,'name' : r.name,'email' : r.email}
        return r
    return decorated_function