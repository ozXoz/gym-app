import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

print("--- CONFIG LOADED ---")
print("MONGO_URI =>", Config.MONGO_URI)
print("JWT_SECRET_KEY =>", Config.JWT_SECRET_KEY[:5], "... (truncated)")
