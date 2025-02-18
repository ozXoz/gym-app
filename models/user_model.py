from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def create_user(data):
    """
    Creates a new user document.
    Defaults role to 'user' if not provided.
    """
    print("--- create_user CALLED ---")
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    role = data.get("role", "user")

    user_doc = {
        "name": data["name"],
        "last_name": data["last_name"],
        "age": data["age"],
        "phone": data["phone"],
        "email": data["email"],
        "password": hashed_password,
        "role": role
    }
    mongo.db.users.insert_one(user_doc)
    print("Inserted user with email:", data["email"])
    print("")
    return user_doc
