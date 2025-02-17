from flask import Flask
from flask_jwt_extended import JWTManager
from config.config import Config
from models.user_model import mongo, bcrypt
from routes.auth_routes import auth

app = Flask(__name__)
app.config.from_object(Config)

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

# Register Blueprint
app.register_blueprint(auth, url_prefix="/api/auth")

@app.route("/")
def index():
    print("GET / -> Returning Hello message")
    return "Hello! Simple Auth with Logging. Use /api/auth/register or /api/auth/login."

if __name__ == "__main__":
    print("--- RUNNING FLASK ---")
    app.run(debug=True)
