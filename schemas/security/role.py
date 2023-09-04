from marshmallow import Schema
from marshmallow.fields import Integer, String


class RoleSchema(Schema):
    id = Integer()
    name = String()
