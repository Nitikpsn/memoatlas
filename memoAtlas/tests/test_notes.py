import unittest
from app import create_app, db
from app.models.user import User
from app.models.note import Note


class NotesTestCase(unittest.TestCase):

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

    def test_notes_index_requires_login(self):
        self.client.get('/auth/logout')
        response = self.client.get('/notes/')
        self.assertEqual(response.status_code, 302)

    def test_notes_index(self):
        response = self.client.get('/notes/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Notes', response.data)

    def test_create_note(self):
        response = self.client.post('/note/new', data={
            'title': 'Test Note',
            'content': 'This is test content.',
            'tags': 'cells, biology'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            note = Note.query.filter_by(title='Test Note').first()
            self.assertIsNotNone(note)
            self.assertEqual(note.is_matched, False)
            self.assertIn('cells', note.tag_list())

    def test_view_note_detail(self):
        with self.app.app_context():
            note = Note(title='Detail Test', content='Detail content', user_id=self.user.id)
            db.session.add(note)
            db.session.commit()
            note_id = note.id

        response = self.client.get(f'/note/{note_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Test', response.data)

    def test_edit_note(self):
        with self.app.app_context():
            note = Note(title='Edit Test', content='Original content', user_id=self.user.id)
            db.session.add(note)
            db.session.commit()
            note_id = note.id

        response = self.client.post(f'/note/{note_id}/edit', data={
            'title': 'Updated Title',
            'content': 'Updated content',
            'tags': 'updated'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            note = db.session.get(Note, note_id)
            self.assertEqual(note.title, 'Updated Title')

    def test_delete_note(self):
        with self.app.app_context():
            note = Note(title='Delete Test', content='To be deleted', user_id=self.user.id)
            db.session.add(note)
            db.session.commit()
            note_id = note.id

        response = self.client.post(f'/note/{note_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            note = db.session.get(Note, note_id)
            self.assertIsNone(note)

    def test_cannot_view_other_user_note(self):
        with self.app.app_context():
            other_user = User(username='other', email='other@example.com')
            other_user.set_password('password123')
            db.session.add(other_user)
            db.session.commit()

            note = Note(title='Private Note', content='Secret', user_id=other_user.id)
            db.session.add(note)
            db.session.commit()
            note_id = note.id

        response = self.client.get(f'/note/{note_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()