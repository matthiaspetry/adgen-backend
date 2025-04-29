from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from supabase import create_client, Client
import os

# Initialize extensions instances (without app context initially)
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://" # Consider changing for production (e.g., redis://localhost:6379/0)
)
supabase: Client = None # Initialize as None

def init_supabase():
    """Initializes the Supabase client using environment variables."""
    global supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise ValueError("Supabase URL and Key must be set in environment variables.")
    supabase = create_client(url, key)

# Function to get the initialized Supabase client
def get_supabase_client() -> Client:
    """Returns the initialized Supabase client instance."""
    if supabase is None:
        init_supabase() # Initialize if not already done
    return supabase
