import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key') # Add a Flask secret key
    DEBUG = False
    TESTING = False
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    # Add other configurations like database URIs, etc.

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Use a separate test database or Supabase project if needed

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Ensure SECRET_KEY is strong and set via environment variable

# Dictionary to access configurations by name
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)

# Function to get Supabase credentials easily
def get_supabase_creds():
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment variables.")
    return url, key
