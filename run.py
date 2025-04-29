import os
from dotenv import load_dotenv

# Load environment variables from .env file before importing the app factory
load_dotenv()

# Import the application factory function from your package
# Corrected import path
from backend import create_app

# Create the Flask app instance using the factory
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

# Run the development server
if __name__ == "__main__":
    # Get host, port, and debug flag from environment variables or use defaults
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    # Ensure FLASK_DEBUG=1 or FLASK_DEBUG=True enables debug mode
    debug = app.config.get('DEBUG', False) # Get debug status from app config

    app.run(host=host, port=port, debug=debug)
