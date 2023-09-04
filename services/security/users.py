from exceptions import AlreadyExistsError
from models.security import User
from schemas.security.user import UserSchema
from services.common.model import ModelService


class UserService(ModelService):
    def __init__(self, session, request_user: User):
        super().__init__(session=session, request_user=request_user ,id_field="id" ,model=User,schema=UserSchema)

    # def get_users(self, user_id=None):
    #     query = self.session.query(User)
    #     if user_id:
    #         query.filter(User.id == user_id)
    #     users = query.all()
    #     return users

    def add_user(self, data):

        login_id = data['login_id']
        user = self.session.query(User).filter(User.login_id == login_id).one_or_none()
        if user:
            raise AlreadyExistsError("User with login id {0} already exists".format(login_id))
        user = User(**data)
        self.session.add(user)
        self.session.commit()
