from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')

def index():
    return render_template('index.html')

@main.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', name=current_user.name)

@main.route('/generateByIngredient')
@login_required
def generateByIngredient():
    return render_template('generateByIngredient.html')

@main.route('/generateByNutrition')
@login_required
def generateByNutrition():
    return render_template('generateByNutrition.html')

@main.route('/mealPlan')
@login_required
def mealPlan():
    return render_template('mealPlan.html')

@main.route('/savedRecipes')
@login_required
def savedRecipes():
    return render_template('savedRecipes.html')

@main.route('/myPreferences')
@login_required
def myPreferences():
    return render_template('myPreferences.html')


