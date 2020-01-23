import os
from flask import Flask
from project.api.views import users_blueprint
from project.api import bcrypt
from database import db, migrate
from flask_cors import CORS


def create_app(script_info=None):
    # Instantiate the app
    app = Flask(__name__)
    CORS(app,supports_credentials=True, resources={r"/api/*": {"origins": "*"}})    # Set Configuration
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    app.register_blueprint(users_blueprint)

    return app
