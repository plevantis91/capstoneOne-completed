from flask import Flask, render_template, flash, jsonify, request, session, redirect, url_for, json, g
import requests
import logging
import os
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm, SearchForm
from flask_migrate import Migrate
from dotenv import load_dotenv
from model import db, User, Recipe
from data import diets, cuisines, intolerances

#Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    
# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Spoonacular API endpoint and API key
SPOONACULAR_API_URL = "https://api.spoonacular.com/recipes/random"
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

# Spoonacular API endpoints
RANDOM_RECIPE_URL = f"https://api.spoonacular.com/recipes/random?apiKey={SPOONACULAR_API_KEY}"
SEARCH_RECIPES_URL = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={SPOONACULAR_API_KEY}"


# Helper functions for Spoonacular API
def fetch_random_recipe():
    try:
        response = requests.get(RANDOM_RECIPE_URL)
        data = response.json()
        return data['recipes'][0] if 'recipes' in data else None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def search_recipes(query,cuisine,diet,intolerance):
    try:
        response = requests.get(f"{SEARCH_RECIPES_URL}&query={query}&cuisine={cuisine}&diet={diet}&intolerance={intolerance}")
        data = response.json()
        return data['results'] if 'results' in data else []
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []

def fetch_recipe_by_id(recipe_id):
    try:
    # Construct the URL to fetch details of a specific recipe by ID
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOONACULAR_API_KEY}"
        # Make the GET request
        response = requests.get(url)
        data = response.json()
        return data
    except (KeyError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")
        return None
    
@app.before_request
def load_logged_in_user():
    g.user = None
    if 'username' in session:
        g.user = User.query.filter_by(username=session['username']).first()

# Index page
@app.route('/')
def start():
    return render_template('index.html')

# Home page
@app.route('/home')
def home_page():
     if g.user:
        liked_recipes = g.user.liked_recipes
        return render_template('home.html', username=g.user.username, liked_recipes=liked_recipes)
     return render_template('index.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different username.')
            return render_template('register.html', form=form, )

        # Create new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        return redirect(url_for('home_page'))

    return render_template('register.html', form=form)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Authenticate users
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('home_page'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home_page'))

# Random recipe route
@app.route('/random_recipe')
def random_recipe():
    if 'username' in session:
        recipe = fetch_random_recipe()
        
        return render_template('recipe.html', recipe=recipe)
    return render_template('home.html')

# Search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        cuisine = form.cuisine.data
        diet = form.diet.data
        intolerance = form.intolerance.data
        recipes = search_recipes(query, cuisine, diet, intolerance)
        return render_template('search.html', username=g.user, 
                               recipes=recipes, form=form, cuisines=cuisines, diets=diets, 
                               intolerances=intolerances)
    return render_template('search.html', username=g.user, 
                           form=form, cuisines=cuisines, diets=diets, 
                           intolerances=intolerances)
                                   
# Recipe details route
@app.route('/search/<int:recipe_id>')
def recipe_details(recipe_id):
    if g.user:
        # Fetch recipe details by ID using the defined function
        recipe = fetch_recipe_by_id(recipe_id)
        
        
        return render_template('recipe.html', recipe=recipe)
   
   
        # Redirect to home page if user is not logged in
    return redirect(url_for('home_page'))

# Save recipe route
@app.route('/like_recipe', methods=['POST'])
def like_recipe():
    try:
        if g.user:
            data = json.loads(request.data.decode('utf-8'))
            recipe_data = data.get('data')

            recipe_id = recipe_data.get('id')

            existing_recipe = Recipe.query.get(recipe_id)

            if existing_recipe: 
                return jsonify({'msg': 'Recipe already liked'}), 200

            else:
                like_recipe = Recipe(
                    id = recipe_data.get('id'),
                    title=recipe_data.get('title', ''),
                    description=recipe_data.get('summary', '')   

                )

                g.user.liked_recipes.append(like_recipe)

                db.session.add(g.user)
                db.session.commit()

                return jsonify({
                    'id': like_recipe.id,
                    'title': like_recipe.title,
                    'description': like_recipe.description  
                })
    except Exception as e:
        logging.error(f"Error liking recipe: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
 
    
#Delete recipe route
@app.route('/delete_recipe', methods=['POST'])
def delete_recipe():
    if g.user:
        data = request.get_json()
        recipe_id = data.get('id')
        
        if recipe_id:
            recipe = Recipe.query.get(recipe_id)
            
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Recipe not found'}), 404
        else:
            return jsonify({'error': 'Invalid data format'}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401
    
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)




