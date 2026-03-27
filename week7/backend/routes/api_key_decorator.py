from flask import request, jsonify
from functools import wraps

ADMIN_API_KEY = "admin-secret-key"

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key != ADMIN_API_KEY:
            return jsonify({"status": "error", "message": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated
