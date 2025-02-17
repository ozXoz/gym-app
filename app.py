from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
from config.config import Config
from models.user_model import mongo, bcrypt
from routes.auth_routes import auth
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS globally

print("--- APP STARTING ---")

# Initialize MongoDB & Bcrypt
mongo.init_app(app)
bcrypt.init_app(app)

# Manually test DB connection here instead of before_first_request
print("--- Testing MongoDB Connection ---")
try:
    test_result = mongo.db.users.find_one()
    print("MongoDB Connection Successful! Found user:", test_result)
except Exception as e:
    print("MongoDB Connection Error:", e)

# JWT Setup
jwt = JWTManager(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # This allows all domains for API routes during testing# Register Blueprint
app.register_blueprint(auth, url_prefix="/api/auth")

@app.route("/")
def index():
    print("GET / -> Returning Hello message")
    return "Hello! Simple Auth with Logging. Use /api/auth/register or /api/auth/login."

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "up"}), 200

if __name__ == "__main__":
    print("--- RUNNING FLASK ---")
    app.run(debug=True)
