# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow cookies for session handling

# Auth decorator
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

@app.route("/protected", methods=["GET"])
@require_auth
def protected():
    user_email = getattr(request.user, 'email', 'unknown') # Access email attribute directly
    return jsonify({"message": f"Hello {user_email}!"})

# Main
if __name__ == "__main__":
    app.run(debug=True)
