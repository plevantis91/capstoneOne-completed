from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import requests

from model import db, Users, Recipes
from data import diets, cuisines, intolerances


app = Flask(__name__)
app.secret_key = 'shhhhhh'

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Spoonacular API endpoint and API key
SPOONACULAR_API_URL = "https://api.spoonacular.com/recipes/random"
SPOONACULAR_API_KEY = "c79bb480382d4aebb082c523481588ee"

# Spoonacular API endpoints
RANDOM_RECIPE_URL = f"https://api.spoonacular.com/recipes/random?apiKey={SPOONACULAR_API_KEY}"
SEARCH_RECIPES_URL = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={SPOONACULAR_API_KEY}"


# Helper functions for Spoonacular API
def fetch_random_recipe():
    response = requests.get(RANDOM_RECIPE_URL)
    data = response.json()
    return data['recipes'][0] if 'recipes' in data else None

def search_recipes(query,cuisine,diet,intolerance):
    response = requests.get(f"{SEARCH_RECIPES_URL}&query={query}&cuisine={cuisine}&diet={diet}&intolerance={intolerance}")
    data = response.json()
    return data['results'] if 'results' in data else []

def fetch_recipe_by_id(recipe_id):
    try:
    # Construct the URL to fetch details of a specific recipe by ID
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOONACULAR_API_KEY}"
        # Make the GET request
        response = requests.get(url)
        print(url) 
        data = response.json()
        return data
    except KeyError as e:
        print(f"{e}")
        return None

# Home page
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/home')
def home_page():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return render_template('index.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if Users.query.filter_by(username=username).first():
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)

        # Create new user
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        return redirect(url_for('home_page'))

    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate users
        user = Users.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return redirect(url_for('home_page'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home_page'))

@app.route('/random_recipe')
def random_recipe():
    if 'username' in session:
        recipe = fetch_random_recipe()
        
        return render_template('recipe.html', recipe=recipe)
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():


     if 'username' in session:
        if request.method == 'POST':
            query = request.form['query']
            cuisine = request.form['cuisine']
            diet = request.form['diet']
            intolerance = request.form['intolerance']
            recipes = search_recipes(query,cuisine,diet,intolerance)
            return render_template('search.html', username=session['username'], 
                                   recipes=recipes, cuisines=cuisines, diets=diets, 
                                   intolerances=intolerances)
     return render_template('search.html', username=session['username'], cuisines=cuisines, diets=diets, 
                                   intolerances=intolerances)

@app.route('/search/<int:recipe_id>')
def recipe_details(recipe_id):
    if 'username' in session:
        # Fetch recipe details by ID using the defined function
        recipe = fetch_recipe_by_id(recipe_id)
        
        
        return render_template('recipe.html', recipe=recipe)
   
   
        # Redirect to home page if user is not logged in
    return redirect(url_for('home_page'))

@app.route('/refresh_recipe')
def refresh_recipe():
    if 'username' in session:
         # Fetch a new random recipe
        recipe = fetch_random_recipe()
    return render_template('recipe.html', username=session['username'], recipe=recipe)

@app.route('/my_recipe')
def my_recipe_page():

# Save recipe route
@app.route('/like_recipe', methods=['POST'])
def like_recipe():
    if 'username' in session:
        username = session['username']
        recipe = request.form['recipe']
        user = Users.query.filter_by(username=username).first()

        if user:
            user.liked_recipes = user.liked_recipes + '\n' + recipe if user.liked_recipes else recipe
            db.session.commit()
            return jsonify({'message': 'Recipe saved successfully'})

    return jsonify({'error': 'User not logged in'})


    

# Other routes for user authentication (login, register, logout) will be added here

if __name__ == '__main__':
    app.run(debug=True)




