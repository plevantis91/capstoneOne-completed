import unittest
from app import app, db, User

class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using the Flask application context
        self.app = app.test_client()
        # Set up the database connection
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/database_name'
        # Initialize SQLAlchemy
        db.init_app(app)
        # Create all tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        # Test the index route without logging in
        response = self.app.get('/')
        self.assertIn(b'Login', response.data)

    def test_login(self):
        # Test the login functionality
        response = self.app.post('/login', data={'username': 'username', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        self.assertIn(b'Welcome', response.data)

    def test_logout(self):
        # Test the logout functionality
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect

    def test_save_recipe(self):
        # Test saving a recipe (requires user to be logged in)
        with self.app as client:
            client.post('/login', data={'username': 'username', 'password': 'password'})
            response = client.post('/save_recipe', data={'recipe': 'Test Recipe'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Recipe saved successfully', response.data)

if __name__ == '__main__':
    unittest.main()
