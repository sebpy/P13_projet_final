import os
import unittest

from app.models import *

TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def login(self, login, password):
        return self.app.post(
            '/login',
            data=dict(username=login, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        response = self.login('admin', 'emoslive')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Connexion', response.data)

    def test_invalid_passwords(self):
        response = self.login('admin', 'emosliv')
        self.assertIn(b'Login ou mot de passe incorrect', response.data)

    def test_invalid_login(self):
        response = self.login('test', 'emoslive')
        self.assertIn(b'Login ou mot de passe incorrect', response.data)


if __name__ == "__main__":
    unittest.main()
