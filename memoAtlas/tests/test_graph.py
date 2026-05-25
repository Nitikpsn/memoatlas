import unittest
from app import create_app, db
from app.models.user import User
from app.models.note import Note
from app.models.connection import Connection
from app.models.progress import Progress
from app.services.graph_service import GraphService


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
            }, follow_redirects=True)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_graph_page_requires_login(self):
        self.client.get('/logout')
        response = self.client.get('/graph')
        self.assertEqual(response.status_code, 302)

    def test_graph_data_empty(self):
        response = self.client.get('/api/graph-data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nodes'], [])
        self.assertEqual(data['links'], [])

    def test_graph_data_with_notes(self):
        with self.app.app_context():
            note = Note(title='Test Note', content='Content', user_id=self.user_id)
            db.session.add(note)
            db.session.commit()

        response = self.client.get('/api/graph-data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['nodes']), 1)
        self.assertEqual(data['nodes'][0]['is_matched'], False)

    def test_create_connection(self):
        with self.app.app_context():
            note1 = Note(title='Note 1', content='Content 1', user_id=self.user_id)
            note2 = Note(title='Note 2', content='Content 2', user_id=self.user_id)
            db.session.add_all([note1, note2])
            db.session.commit()

            conn = GraphService.create_connection(
                self.user_id, note1.id, note2.id, 'related to'
            )
            self.assertIsNotNone(conn)
            self.assertEqual(conn.source_note_id, note1.id)
            self.assertEqual(conn.target_note_id, note2.id)

            self.assertTrue(db.session.get(Note, note1.id).is_matched)
            self.assertTrue(db.session.get(Note, note2.id).is_matched)

    def test_get_connected_notes(self):
        with self.app.app_context():
            note1 = Note(title='Note 1', content='Content 1', user_id=self.user_id)
            note2 = Note(title='Note 2', content='Content 2', user_id=self.user_id)
            note3 = Note(title='Note 3', content='Content 3', user_id=self.user_id)
            db.session.add_all([note1, note2, note3])
            db.session.commit()

            GraphService.create_connection(self.user_id, note1.id, note2.id)
            GraphService.create_connection(self.user_id, note1.id, note3.id)

            connected = GraphService.get_connected_notes(note1.id, self.user_id)
            self.assertEqual(len(connected), 2)

    def test_link_api(self):
        note_ids = []
        with self.app.app_context():
            note1 = Note(title='Note 1', content='Content 1', user_id=self.user_id)
            note2 = Note(title='Note 2', content='Content 2', user_id=self.user_id)
            db.session.add_all([note1, note2])
            db.session.commit()
            note_ids = [note1.id, note2.id]

        response = self.client.post('/api/link', json={
            'source_id': note_ids[0],
            'target_id': note_ids[1]
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['xp_gained'], 100)


if __name__ == '__main__':
    unittest.main()
