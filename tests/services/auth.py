import unittest
from unittest import TestCase
from unittest.mock import Mock

from exceptions import AuthenticationError, DoNotExistsError, NotActiveError
from models.security import User
from services.security.auth import Authenticator


# def setUpModule():
#     print('Running setUpModule')
#
#
# def tearDownModule():
#     print('Running tearDownModule')

class TestAuthenticator(TestCase):
    users = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.users = {'admin': User(login_id="admin", password="admin", is_active='Y'),
                     'ramesh': User(login_id="ramesh", password="ramesh", is_active='N')}

    def setUp(self):
        self.mock_db_session = Mock(name="Mock db session")
        self.auth_service = Authenticator(session=self.mock_db_session)

    def test_authenticate_valid(self):
        # self.mock_db_session.query.return_value.filter.return_value.one_or_none.return_value = User(login_id="admin",password="admin")
        filter_mock = self.mock_db_session.query().filter
        filter_mock().one_or_none.return_value = TestAuthenticator.users.get('admin')
        user = self.auth_service.authenticate(login_id="admin", password="admin")
        filter_mock.assert_called_with((User.login_id == "admin"))
        self.assertIsNotNone(user)
        self.assertEqual(user.login_id, "admin")

    def test_authenticate_invalid(self):
        self.mock_db_session.query().filter().one_or_none.return_value = TestAuthenticator.users.get('admin')
        with self.assertRaises(AuthenticationError):
            self.auth_service.authenticate(login_id="admin", password="admi")

    def test_authenticate_notexists(self):
        self.mock_db_session.query().filter().one_or_none.return_value = None
        with self.assertRaises(DoNotExistsError):
            self.auth_service.authenticate(login_id="admi", password="admi")

    def test_authenticate_inactive(self):
        self.mock_db_session.query().filter().one_or_none.return_value = TestAuthenticator.users.get('ramesh')
        with self.assertRaises(NotActiveError):
            self.auth_service.authenticate(login_id="ramesh", password="ram")

    # @classmethod
    # def tearDownClass(cls):
    #     print('Running tearDownClass')
    #
    # def tearDown(self):
    #     print('Running tearDown')


if __name__ == '__main__':
    unittest.main()
