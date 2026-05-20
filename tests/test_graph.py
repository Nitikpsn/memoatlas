import unittest
from app import create_app, db
from app.models.user import User
from app.models.note import Note
from app.models.connection import Connection
from app.services.graph_service import GraphService


class GraphTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            self.user = user
            self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_graph_page_requires_login(self):
        self.client.get('/auth/logout')
        response = self.client.get('/graph/')
        self.assertEqual(response.status_code, 302)

    def test_graph_data_empty(self):
        response = self.client.get('/graph/data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nodes'], [])
        self.assertEqual(data['edges'], [])

    def test_graph_data_with_notes(self):
        with self.app.app_context():
            note = Note(title='Test Note', content='Content', user_id=self.user.id)
            db.session.add(note)
            db.session.commit()

        response = self.client.get('/graph/data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['nodes']), 1)

    def test_create_connection(self):
        with self.app.app_context():
            note1 = Note(title='Note 1', content='Content 1', user_id=self.user.id)
            note2 = Note(title='Note 2', content='Content 2', user_id=self.user.id)
            db.session.add_all([note1, note2])
            db.session.commit()

            conn = GraphService.create_connection(
                self.user.id, note1.id, note2.id, 'related to'
            )
            self.assertIsNotNone(conn)
            self.assertEqual(conn.source_note_id, note1.id)
            self.assertEqual(conn.target_note_id, note2.id)

    def test_get_connected_notes(self):
        with self.app.app_context():
            note1 = Note(title='Note 1', content='Content 1', user_id=self.user.id)
            note2 = Note(title='Note 2', content='Content 2', user_id=self.user.id)
            note3 = Note(title='Note 3', content='Content 3', user_id=self.user.id)
            db.session.add_all([note1, note2, note3])
            db.session.commit()

            GraphService.create_connection(self.user.id, note1.id, note2.id)
            GraphService.create_connection(self.user.id, note1.id, note3.id)

            connected = GraphService.get_connected_notes(note1.id, self.user.id)
            self.assertEqual(len(connected), 2)


if __name__ == '__main__':
    unittest.main()
