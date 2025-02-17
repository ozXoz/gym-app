from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user_model import mongo, bcrypt, create_user

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    print("--- REGISTER ROUTE CALLED ---")

    data = request.json
    print("Incoming data:", data)

    required_fields = ["name", "last_name", "age", "phone", "email", "password"]
    if not data or not all(field in data for field in required_fields):
        print("Missing fields -> 400")
        return jsonify({"message": "Missing fields"}), 400

    existing_user = mongo.db.users.find_one({"email": data["email"]})
    print("Existing user check:", existing_user)

    if existing_user:
        print("Email already registered -> 400")
        return jsonify({"message": "Email already registered"}), 400

    create_user(data)
    print("User registered successfully -> 201")
    return jsonify({"message": "Registration successful."}), 201


@auth.route("/login", methods=["POST"])
def login():
    print("--- LOGIN ROUTE CALLED ---")

    data = request.json
    print("Incoming data:", data)

    if not data or "email" not in data or "password" not in data:
        print("Missing email or password -> 400")
        return jsonify({"message": "Missing email or password"}), 400

    user = mongo.db.users.find_one({"email": data["email"]})
    print("User found in DB:", user)

    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        print("Invalid credentials -> 401")
        return jsonify({"message": "Invalid credentials"}), 401

    print("Credentials valid. Generating JWT.")
    access_token = create_access_token(identity={"email": user["email"], "role": user["role"]})
    return jsonify({"token": access_token, "role": user["role"]}), 200

@auth.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    print("--- ADMIN ROUTE CALLED ---")
    current_user = get_jwt_identity()
    print("Current user:", current_user)

    if current_user["role"] != "admin":
        print("Role is not admin -> 403")
        return jsonify({"message": "Unauthorized"}), 403

    print("Welcome Admin -> 200")
    return jsonify({"message": "Welcome, Admin!"}), 200
