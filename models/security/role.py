from sqlalchemy import Column, Integer, String, Table, ForeignKey

from db.services.context import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


user_role_map = Table(
    "user_role_maps",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id")),
)
