import logging

from exceptions import DoNotExistsError, NotActiveError, AuthenticationError
from models.security.user import User

logger = logging.getLogger(__name__)


class Authenticator(object):
    def __init__(self, session):
        self.session = session

    def authenticate(self, login_id, password):
        user = self.session.query(User).filter(User.login_id == login_id).one_or_none()

        if not user:
            msg = "User with login id {0} doesn't exists.".format(login_id)
            logger.debug(msg)
            raise DoNotExistsError(msg)
        if user.is_active == 'N':
            msg = "User with login id {0} is not active.".format(login_id)
            logger.debug(msg)
            raise NotActiveError(msg)
        if user.password == password:
            return user
        else:
            msg = "Authentication failed for user with login id {0}.".format(login_id)
            logger.debug(msg)
            raise AuthenticationError(msg)
