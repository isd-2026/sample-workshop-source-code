from flask import Blueprint, jsonify, request
from backend.models.db_crud import get_user_by_email,add_user

auth_bp = Blueprint("auth",__name__)

@auth_bp.route('/login',methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # server-side validation
    if not email or not password:
        return jsonify({"status":"error", "message":"Email and password required"}), 400

    user_row = get_user_by_email(email) # returns a tuple not an object
    if user_row is None:
        return jsonify({"status":"error", "message": "Email doesn't exist. Please register."}), 404
    
    if user_row["password"] != password:
        return jsonify({"status":"error", "message": "Incorrect password."}), 401
    
    return jsonify({
        "status": "success",
        "message": "Login successful",
        "user": {
            "name": user_row["name"],
            "email": user_row["email"],
            "gender": user_row["gender"],
            "favcol": user_row["favcol"]
        }
    }), 200

@auth_bp.route('/register',methods=["POST"])
def register():
    data = request.json

    # Check if user already exists
    if get_user_by_email(data["email"]) is not None:
        return jsonify({"status":"error", "message": f"Email '{data['email']}' already exists"}), 409

    try:
        add_user(data["name"], data["email"], data["password"],data["gender"], data["favcol"])
        return jsonify({
            "status":"success",
            "message": f"User {data['name']} added successfully",
            "user": {
                "name": data["name"],
                "email": data["email"],
                "gender": data["gender"],
                "favcol": data["favcol"]
            }
        }), 201
    except ValueError as e:
        # catch duplicate email from DB constraint
        return jsonify({"status":"error", "message": str(e)}), 400