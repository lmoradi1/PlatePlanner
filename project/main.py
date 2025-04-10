from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import FavoriteRecipe

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

@main.route('/add-favorite', methods=['POST'])
@login_required
def add_favorite():
    data = request.get_json()
    recipe_id = data.get('recipeId')
    title = data.get('title')
    image = data.get('image')

    # Check if already saved
    existing = FavoriteRecipe.query.filter_by(recipe_id=recipe_id, user_id=current_user.id).first()
    if existing:
        return jsonify({"message": "Already in favorites"}), 409

    new_fav = FavoriteRecipe(recipe_id=recipe_id, title=title, image=image, user_id=current_user.id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"message": "Added to favorites"}), 200
