# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from supabase import create_client
import os
from dotenv import load_dotenv
# Import Flask-Limiter components
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address, # Use the client's IP address as the key
    app=app,
    default_limits=["200 per day", "50 per hour"], # Example default limits for all routes
    storage_uri="memory://" # Use in-memory storage (consider Redis for production)
)

# Auth decorator
# Apply a stricter limit specifically to authentication checks if desired
# Note: Applying it here would limit *any* route using @require_auth
# It might be better to apply limits directly on the routes themselves.
# @limiter.limit("10 per minute") # Example: Limit auth checks
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Try to get token from cookies or Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            token = request.cookies.get('sb-access-token')

        if not token:
            return jsonify({"error": "Missing access token"}), 401

        try:
            response = supabase.auth.get_user(token)
            # Check if the user object exists directly on the response
            if response and response.user:
                request.user = response.user  # Attach user to request
            else:
                # Log the actual response for debugging if needed
                print("Auth Response:", response)
                return jsonify({"error": "Invalid or expired token"}), 401
        except Exception as e:
            print("Auth Error:", str(e))
            return jsonify({"error": "Authentication failed"}), 401

        return f(*args, **kwargs)
    return decorated

# Routes

@app.route("/")
def index():
    return jsonify({"message": "Backend is live"})

# Apply rate limit to the protected route
@app.route("/protected", methods=["GET"])
@limiter.limit("15 per minute") # Example: Limit this specific route
@require_auth
def protected():
    print(request.user.id)
    user_email = getattr(request.user, 'email', 'unknown')
    return jsonify({"message": f"Hello {user_email}!"})

# You might also want to rate limit login/signup routes if you add them

# Main
if __name__ == "__main__":
    app.run(debug=True)
