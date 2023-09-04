from marshmallow import Schema
from marshmallow.fields import String, Integer, Nested

from schemas.security.role import RoleSchema


class UserSchema(Schema):
    id = Integer()
    login_id = String()
    name = String()
    is_active = String()
    roles = Nested(RoleSchema(),many=True)
