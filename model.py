from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    liked_recipes = db.Column(db.Text)

    # Define relationship with Recipe table
    recipes = db.relationship('Recipes', backref='users', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Recipe {self.title}>'


# session
# routing
# query db
    
    # protecting routes 
    # redirect 

