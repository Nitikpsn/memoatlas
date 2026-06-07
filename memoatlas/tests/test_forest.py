import unittest
from memoatlas import create_app
from memoatlas.models import db, User, Tree


class ForestTestCase(unittest.TestCase):

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

    def test_dashboard_requires_login(self):
        self.client.get('/logout')
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_dashboard(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_plant_tree(self):
        r = self.client.post('/plant', data={
            'title': 'Test Tree',
            'content': 'Test content',
            'tags': 'test, tree'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)

        with self.app.app_context():
            t = Tree.query.filter_by(title='Test Tree').first()
            self.assertIsNotNone(t)
            self.assertNotEqual(t.health_score, 0)

    def test_view_tree(self):
        tree_id = None
        with self.app.app_context():
            t = Tree(title='Detail', content='Content', user_id=self.user_id)
            db.session.add(t)
            db.session.commit()
            tree_id = t.id

        r = self.client.get('/tree/' + str(tree_id))
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Detail', r.data)

    def test_edit_tree(self):
        tree_id = None
        with self.app.app_context():
            t = Tree(title='Before', content='Old', user_id=self.user_id)
            db.session.add(t)
            db.session.commit()
            tree_id = t.id

        r = self.client.post('/tree/' + str(tree_id) + '/edit', data={
            'title': 'After',
            'content': 'New content',
            'tags': 'updated'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)

        with self.app.app_context():
            t = db.session.get(Tree, tree_id)
            self.assertEqual(t.title, 'After')

    def test_delete_tree(self):
        tree_id = None
        with self.app.app_context():
            t = Tree(title='Delete', content='Me', user_id=self.user_id)
            db.session.add(t)
            db.session.commit()
            tree_id = t.id

        r = self.client.post('/tree/' + str(tree_id) + '/delete', follow_redirects=True)
        self.assertEqual(r.status_code, 200)

        with self.app.app_context():
            t = db.session.get(Tree, tree_id)
            self.assertIsNone(t)

    def test_cannot_view_other_tree(self):
        tree_id = None
        with self.app.app_context():
            other = User(username='other', email='other@example.com')
            other.set_password('password123')
            db.session.add(other)
            db.session.commit()
            t = Tree(title='Private', content='Secret', user_id=other.id)
            db.session.add(t)
            db.session.commit()
            tree_id = t.id

        r = self.client.get('/tree/' + str(tree_id))
        self.assertEqual(r.status_code, 403)


if __name__ == '__main__':
    unittest.main()
