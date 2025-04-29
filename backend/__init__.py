from flask import Flask
import os

# Import configurations
from config import config_by_name

# Import extensions
from .extentions import cors, limiter, init_supabase

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions with the app
    cors.init_app(app, supports_credentials=True) # Ensure CORS is initialized correctly
    limiter.init_app(app)
    init_supabase() # Initialize the Supabase client

    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Add other blueprints here (e.g., auth, api)

    return app
