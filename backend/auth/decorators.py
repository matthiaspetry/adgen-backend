from functools import wraps
from flask import request, jsonify

# Import the Supabase client getter from extensions
from ..extentions import get_supabase_client

def require_auth(f):
    """Decorator to ensure the user is authenticated via Supabase token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        supabase = get_supabase_client() # Get the initialized client

        # Try to get token from cookies or Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
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
            # Return a generic error in production
            return jsonify({"error": "Authentication failed"}), 401

        return f(*args, **kwargs)
    return decorated
