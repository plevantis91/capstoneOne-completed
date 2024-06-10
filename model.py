from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserRecipe(db.Model):
    __tablename__ = 'user_recipes'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True) 
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # Define relationship with Recipe table
    liked_recipes = db.relationship('Recipe', secondary='user_recipes', backref='users')

    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
   

    def __repr__(self):
        return f'<Recipe {self.title}>'
    

def connect_db(app):

    db.app = app
    db.init_app(app)





