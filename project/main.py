from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import FavoriteRecipe, UserPreferences

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

    existing = FavoriteRecipe.query.filter_by(recipe_id=recipe_id, user_id=current_user.id).first()
    if existing:
        return jsonify({"message": "Already in favorites"}), 409

    new_fav = FavoriteRecipe(recipe_id=recipe_id, title=title, image=image, user_id=current_user.id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"message": "Added to favorites"}), 200

@main.route('/get-favorites')
@login_required
def get_favorites():
    favorites = FavoriteRecipe.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {"recipe_id": fav.recipe_id, "title": fav.title, "image": fav.image}
        for fav in favorites
    ])

@main.route('/remove-favorite', methods=['POST'])
@login_required
def remove_favorite():
    data = request.get_json()
    recipe_id = data.get('recipeId')

    to_delete = FavoriteRecipe.query.filter_by(recipe_id=recipe_id, user_id=current_user.id).first()
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
        return jsonify({"message": "Removed from favorites"}), 200
    else:
        return jsonify({"message": "Recipe not found in favorites"}), 404

@main.route('/get-preferences')
@login_required
def get_preferences():
    prefs = current_user.preferences
    if not prefs:
        return jsonify({
            "gluten_free": False,
            "dairy_free": False,
            "soy_free": False,
            "egg_free": False,
            "nut_free": False,
            "sugar_free": False
        })
    return jsonify({
        "gluten_free": prefs.gluten_free,
        "dairy_free": prefs.dairy_free,
        "soy_free": prefs.soy_free,
        "egg_free": prefs.egg_free,
        "nut_free": prefs.nut_free,
        "sugar_free": prefs.sugar_free
    })

@main.route('/save-preferences', methods=['POST'])
@login_required
def save_preferences():
    data = request.get_json()
    prefs = current_user.preferences

    if not prefs:
        prefs = UserPreferences(user_id=current_user.id)

    prefs.gluten_free = data.get('gluten_free', False)
    prefs.dairy_free = data.get('dairy_free', False)
    prefs.soy_free = data.get('soy_free', False)
    prefs.egg_free = data.get('egg_free', False)
    prefs.nut_free = data.get('nut_free', False)
    prefs.sugar_free = data.get('sugar_free', False)

    db.session.add(prefs)
    db.session.commit()
    return jsonify({"message": "Preferences saved!"})
