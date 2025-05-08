import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create the SQLAlchemy instance once
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Set secret key from environment or fallback (safe for dev)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

    # Determine environment type
    environment = os.getenv('FLASK_ENV', 'development')

    # Set appropriate database URI
    if environment == 'production':
        database_password = os.getenv('DATABASE_PASSWORD')
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'mysql+mysqlconnector://admin:{database_password}'
            f'@database-1.ce3g3fiuk5qg.us-east-1.rds.amazonaws.com/PlatePlanner'
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Set track modifications to False to avoid warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Optional debug info (only print after all config is set)
    print(f"[DEBUG] Environment: {environment}")
    print(f"[DEBUG] Using DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import models AFTER db.init_app to avoid circular import issues
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register authentication blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Register main application blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Optional route to return your API key
    @app.route("/get-api-key")
    def get_api_key():
        return jsonify({"api_key": os.getenv("SPOONACULAR_API_KEY")})

    return app
