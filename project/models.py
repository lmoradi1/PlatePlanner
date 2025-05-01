from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    favorites = db.relationship('FavoriteRecipe', backref='user', lazy=True)
    preferences = db.relationship('UserPreferences', backref='user', uselist=False)
    meal_plan = db.relationship('MealPlanEntry', backref='user', lazy=True)


class FavoriteRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    gluten_free = db.Column(db.Boolean, default=False)
    dairy_free = db.Column(db.Boolean, default=False)
    soy_free = db.Column(db.Boolean, default=False)
    egg_free = db.Column(db.Boolean, default=False)
    nut_free = db.Column(db.Boolean, default=False)
    sugar_free = db.Column(db.Boolean, default=False)

class MealPlanEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # e.g., "Monday"
    meal_type = db.Column(db.String(20), nullable=False)    # "main" or "side"
    category = db.Column(db.String(50))                    # e.g., "chicken", "fish"
    recipe_id = db.Column(db.Integer, nullable=False)
    recipe_title = db.Column(db.String(255))
    recipe_image = db.Column(db.String(255))

