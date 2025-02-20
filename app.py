from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from config.config import Config
from models.user_model import mongo, bcrypt
from routes.auth_routes import auth
from routes.forgot_password import forgot_password_bp
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Enable debugging
app.debug = True
app.logger.setLevel(logging.DEBUG)

# Fix CORS Policy
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Flask-Mail
mail = Mail(app)

print("--- APP STARTING ---")

# Initialize MongoDB & Bcrypt
mongo.init_app(app)
bcrypt.init_app(app)

# JWT Setup
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(forgot_password_bp, url_prefix="/api/auth")

@app.route("/")
def index():
    return "Hello! Use /api/auth/register or /api/auth/login."

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "up"}), 200

if __name__ == "__main__":
    print("--- RUNNING FLASK ---")
    app.run(debug=True)
