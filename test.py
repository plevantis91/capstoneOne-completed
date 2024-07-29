import unittest
from app import app, db, User, Recipe, bcrypt
from flask import json

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test client and create the database schema."""
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_one_test'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Drop the database schema after tests are done."""
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        """Create a user and other setup before each test."""
        with self.app.app_context():
            # Create a user for testing
            self.user = User(username='testuser', password=bcrypt.generate_password_hash('password').decode('utf-8'))
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Recipe App', response.data)

    def test_login(self):
        response = self.client.post('/login', data=dict(username='testuser', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_register(self):
        response = self.client.post('/register', data=dict(username='newuser', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful!', response.data)

    def test_logout(self):
        self.client.post('/login', data=dict(username='testuser', password='password'))
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)

    def test_random_recipe(self):
        self.client.post('/login', data=dict(username='testuser', password='password'))
        response = self.client.get('/random_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe Details', response.data)

    def test_search(self):
        response = self.client.post('/search', data=dict(query='chicken', cuisine='Italian', diet='Vegetarian', intolerance='Gluten'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results', response.data)

    def test_recipe_details(self):
        # Mock a recipe ID for testing
        recipe_id = 1
        response = self.client.get(f'/search/{recipe_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe Details', response.data)

    def test_like_recipe(self):
        self.client.post('/login', data=dict(username='testuser', password='password'))
        response = self.client.post('/like_recipe', data=json.dumps({'data': {'id': 1, 'title': 'Test Recipe', 'summary': 'Test Description'}}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Recipe', response.data)

    def test_delete_recipe(self):
        self.client.post('/login', data=dict(username='testuser', password='password'))
        response = self.client.post('/delete_recipe', data=json.dumps({'id': 1}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

if __name__ == '__main__':
    unittest.main()
