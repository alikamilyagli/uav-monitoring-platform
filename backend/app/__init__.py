import logging
import os
from flask import Flask, current_app
from flask_cors import CORS
from config import Config
from .extensions import db, auth
from .routes import api_bp
from .services import DroneService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
    configure_logging(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()
        DroneService.seed_initial_drones()

    return app

def configure_logging(app):
    app.logger.setLevel(logging.DEBUG)

def register_blueprints(app):
    app.register_blueprint(api_bp)

@auth.verify_password
def verify_password(username, password):
    expected_username = os.getenv('ADMIN_USERNAME', 'admin')
    expected_password = os.getenv('ADMIN_PASSWORD', 'admin')

    if username == expected_username and password == expected_password:
        current_app.logger.debug(f"User {username} authenticated successfully")
        return username

    current_app.logger.warning(f"Authentication failed for user {username}")
    return None
