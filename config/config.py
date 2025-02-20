import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    MAIL_SERVER = 'smtp.gmail.com'   # Use Gmail SMTP
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Set in .env
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # Set in .env

print("--- CONFIG LOADED ---")
print("MONGO_URI =>", Config.MONGO_URI)
print("JWT_SECRET_KEY =>", Config.JWT_SECRET_KEY[:5], "... (truncated)")
