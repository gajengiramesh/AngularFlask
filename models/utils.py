from sqlalchemy import Column, Integer, String, DateTime , func


def current_user_id():
    return 1

class CreatedMixin(object):

    created_on = Column(DateTime,default=func.now())
    created_by = Column(Integer,default=current_user_id)