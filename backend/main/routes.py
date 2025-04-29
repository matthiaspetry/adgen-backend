from flask import jsonify, request

# Import the main blueprint
from . import main

# Import the limiter instance from extensions
from ..extentions import limiter

# Import the auth decorator
from ..auth.decorators import require_auth

@main.route("/")
def index():
    """Index route."""
    return jsonify({"message": "Backend is live"})

@main.route("/protected", methods=["GET"])
@limiter.limit("15 per minute") # Apply rate limit
@require_auth # Apply authentication check
def protected():
    """Protected route example."""
    # Access user ID and email from the request object populated by require_auth
    user_id = getattr(request.user, 'id', 'unknown')
    user_email = getattr(request.user, 'email', 'unknown')
    print(f"Accessing protected route for user ID: {user_id}")
    return jsonify({"message": f"Hello {user_email}!", "user_id": user_id})

# Add other main routes here
