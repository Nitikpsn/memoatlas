import unittest
from app import create_app
from app.models import db, User


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(dict(
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            WTF_CSRF_ENABLED=False
        ))
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page(self):
        r = self.client.get('/login')
        self.assertEqual(r.status_code, 200)

    def test_register_page(self):
        r = self.client.get('/register')
        self.assertEqual(r.status_code, 200)

    def test_landing_page(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_login_success(self):
        r = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)

    def test_login_failure(self):
        r = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrong'
        })
        self.assertEqual(r.status_code, 302)

    def test_register_success(self):
        r = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm': 'password123'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)

    def test_register_duplicate_username(self):
        r = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'password123',
            'confirm': 'password123'
        })
        self.assertEqual(r.status_code, 302)

    def test_logout(self):
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        r = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
