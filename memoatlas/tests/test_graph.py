import unittest
from memoatlas import create_app
from memoatlas.models import db, User, Tree, Connection, Progress


class GraphTestCase(unittest.TestCase):

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
            self.user_id = user.id
            self.client.post('/login', data={
                'email': 'test@example.com',
                'password': 'password123'
            })

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_graph_page_requires_login(self):
        self.client.get('/logout')
        r = self.client.get('/map')
        self.assertEqual(r.status_code, 302)

    def test_graph_data_empty(self):
        r = self.client.get('/api/graph-data')
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data['nodes'], [])
        self.assertEqual(data['links'], [])

    def test_graph_data_with_trees(self):
        with self.app.app_context():
            t = Tree(title='Test', content='Content', user_id=self.user_id)
            db.session.add(t)
            db.session.commit()

        r = self.client.get('/api/graph-data')
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(len(data['nodes']), 1)

    def test_create_connection(self):
        with self.app.app_context():
            t1 = Tree(title='A', content='A', user_id=self.user_id)
            t2 = Tree(title='B', content='B', user_id=self.user_id)
            db.session.add_all([t1, t2])
            db.session.commit()

            conn = Connection(source_id=t1.id, target_id=t2.id, user_id=self.user_id)
            db.session.add(conn)
            db.session.commit()

            self.assertIsNotNone(conn.id)

    def test_link_api(self):
        ids = []
        with self.app.app_context():
            t1 = Tree(title='One', content='One', user_id=self.user_id)
            t2 = Tree(title='Two', content='Two', user_id=self.user_id)
            db.session.add_all([t1, t2])
            db.session.commit()
            ids = [t1.id, t2.id]

        r = self.client.post('/api/link', json={
            'source_id': ids[0],
            'target_id': ids[1]
        })
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data['xp_gained'], 100)


if __name__ == '__main__':
    unittest.main()
