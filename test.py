import unittest
import json
from app import app, db, User, Recipe

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Set up a test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        db.create_all()
        
        # Create a test user
        self.test_user = User(username='testuser', password='password')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_register(self):
        response = self.app.post('/register', data=dict(
            username='newuser',
            password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)

    def test_login(self):
        response = self.login('testuser', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser', response.data)

    def test_random_recipe(self):
        self.login('testuser', 'password')
        response = self.app.get('/random_recipe')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'recipe', response.data)

    def test_like_recipe(self):
        self.login('testuser', 'password')
        recipe_data = {
            'data': {
                'id': 1,
                'title': 'Test Recipe',
                'summary': 'Test Description'
            }
        }
        response = self.app.post('/like_recipe', data=json.dumps(recipe_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        liked_recipe = Recipe.query.get(1)
        self.assertIsNotNone(liked_recipe)
        self.assertEqual(liked_recipe.title, 'Test Recipe')

    def test_delete_recipe(self):
        self.login('testuser', 'password')
        recipe = Recipe(id=1, title='Test Recipe', description='Test Description')
        self.test_user.liked_recipes.append(recipe)
        db.session.commit()
        
        response = self.app.post('/delete_recipe', data=json.dumps({'id': 1}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data)['success'])
        deleted_recipe = Recipe.query.get(1)
        self.assertIsNone(deleted_recipe)

if __name__ == '__main__':
    unittest.main()
