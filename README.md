Description
Recipe App is a web application that allows users to browse and manage recipes. Users can search for recipes based on various criteria, view detailed recipe information, and save their favorite recipes. The app integrates with the Spoonacular API to fetch and search for recipes.

Features
User Registration and Login: Users can create an account and log in to access personalized features.
Recipe Search: Users can search for recipes by ingredients, cuisine, diet, and intolerance using the Spoonacular API.
Random Recipe Generator: Users can get a random recipe recommendation.
Recipe Details: Users can view detailed information about a specific recipe.
Save Favorite Recipes: Users can save and manage their favorite recipes.
Delete Favorite Recipes: Users can remove recipes from their list of favorites.
User Flow
Home Page: Users are welcomed with the home page. Logged-in users can see their saved recipes.
Registration: Users can sign up by providing a username and password. Existing users are alerted to choose a different username.
Login: Users can log in with their credentials. If authentication fails, they receive an error message.
Search Recipes: Users can search for recipes using various filters (query, cuisine, diet, intolerance). The results are displayed based on the search criteria.
View Recipe Details: Users can click on a recipe to view detailed information.
Save Recipes: Users can save recipes to their favorites. If the recipe is already saved, they receive a notification.
Delete Recipes: Users can remove recipes from their saved list.
Logout: Users can log out, which ends their session and redirects them to the home page.
API
The application uses the Spoonacular API for recipe data. Below are the main endpoints:

Random Recipe: https://api.spoonacular.com/recipes/random?apiKey=<YOUR_API_KEY>
Retrieves a random recipe.
Search Recipes: https://api.spoonacular.com/recipes/complexSearch?apiKey=<YOUR_API_KEY>&query=<QUERY>&cuisine=<CUISINE>&diet=<DIET>&intolerance=<INTOLERANCE>
Searches for recipes based on query parameters.
Recipe Details: https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey=<YOUR_API_KEY>
Fetches details of a specific recipe by ID.
Notes:

Ensure to replace <YOUR_API_KEY> with your actual API key.
Be aware of API rate limits and usage restrictions as per the Spoonacular API documentation.
Technology Stack
Frontend:
HTML/CSS/JavaScript
Bootstrap (for styling, if used)
Backend:
Flask - Web framework for server-side logic
Flask-SQLAlchemy - ORM for database management
Flask-Bcrypt - For password hashing
Flask-Migrate - Database migrations
Database:
PostgreSQL - Database management system
APIs:
Spoonacular API - For recipe data
Development Tools:
Python - Programming language
Git - Version control system
Heroku/GitHub/Other - Deployment and version control

git clone https://github.com/plevantis91/capstoneOne-completed.git
cd capstoneOne-completed

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
SPOONACULAR_API_KEY=your_spoonacular_api_key

flask db init
flask db migrate
flask db upgrade

flask run



