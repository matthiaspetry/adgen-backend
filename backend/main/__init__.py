from flask import Blueprint

# Create the main blueprint instance
main = Blueprint('main', __name__)

# Import routes after creating the blueprint to avoid circular imports
from . import routes
