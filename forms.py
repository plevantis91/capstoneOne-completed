from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length
from data import diets, cuisines, intolerances

class RegisterForm(FlaskForm):
    """Form for registering a user."""
    
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=100)])
    SubmitField = SubmitField("Submit")
    
class LoginForm(FlaskForm):
    """Form for logging in a user."""
    
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=100)])
    SubmitField = SubmitField("Submit")
    
class SearchForm(FlaskForm):
    """Form for searching for a recipe."""
    
    query = StringField('Query')
    cuisine = SelectField('Cuisine:', choices=[('', 'Select cuisine...')] + [(cuisine, cuisine) for cuisine in cuisines])
    diet = SelectField('Diet:', choices=[('', 'Select diet...')] + [(diet, diet) for diet in diets])
    intolerance = SelectField('Allergies:', choices=[('', 'Select intolerance...')] + [(intolerance, intolerance) for intolerance in intolerances])
    submit = SubmitField('Search')