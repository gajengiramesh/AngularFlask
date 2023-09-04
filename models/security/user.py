from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db.services.context import Base
from models.security.role import user_role_map
from models.utils import CreatedMixin




class User(Base,CreatedMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login_id = Column(String(50), unique=True)
    password = Column(String(50))
    name = Column(String(50))
    email = Column(String(120), unique=True)
    is_active = Column(String(1), default='Y')

    roles = relationship(
        "Role", secondary=user_role_map, backref="users",uselist=True
    )
