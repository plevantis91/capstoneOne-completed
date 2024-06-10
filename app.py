from flask import Flask, render_template, jsonify, request, session, redirect, url_for, json
import requests
import logging

from model import db, User, Recipe
from data import diets, cuisines, intolerances


app = Flask(__name__)
app.secret_key = 'shhhhhh'

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_one'
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

# Index page
@app.route('/')
def start():
    return render_template('index.html')

# Home page
@app.route('/home')
def home_page():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            liked_recipes = user.liked_recipes
        return render_template('home.html', username=session['username'], liked_recipes=liked_recipes)
    return render_template('index.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)

        # Create new user
        new_user = User(username=username, password=password)
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
        user = User.query.filter_by(username=username, password=password).first()

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
                                   
# Recipe details route
@app.route('/search/<int:recipe_id>')
def recipe_details(recipe_id):
    if 'username' in session:
        # Fetch recipe details by ID using the defined function
        recipe = fetch_recipe_by_id(recipe_id)
        
        
        return render_template('recipe.html', recipe=recipe)
   
   
        # Redirect to home page if user is not logged in
    return redirect(url_for('home_page'))

# Save recipe route
@app.route('/like_recipe', methods=['POST'])
def like_recipe():
    try:
        if 'username' in session:
            username = session['username']
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

                user = User.query.filter_by(username=username).first()
                if user:
                    user.liked_recipes.append(like_recipe)

                    db.session.add(user)
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
    if 'username' in session:
        username = session['username']
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




