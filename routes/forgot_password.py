from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, decode_token
from flask_mail import Mail, Message
from datetime import timedelta
from models.user_model import mongo, bcrypt
import os

forgot_password_bp = Blueprint("forgot_password", __name__)
mail = Mail()

def send_reset_email(email, token):
    """Send password reset email to the user."""
    try:
        reset_link = f"https://yourfrontend.com/reset-password?token={token}"

        msg = Message(
            "Password Reset Request",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email]
        )

        msg.body = f"""
        Hi,

        Click the link below to reset your password:

        {reset_link}

        If you did not request this, ignore this email.

        Regards,
        Your App Team
        """

        mail.send(msg)
        print(f"✅ Email sent to: {email}")

    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")


@forgot_password_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """Handles password reset requests."""
    try:
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"message": "Email is required"}), 400

        user = mongo.db.users.find_one({"email": email})
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Generate password reset token (expires in 15 minutes)
        reset_token = create_access_token(
            identity={"email": email},
            expires_delta=timedelta(minutes=15)
        )

        print(f"🔹 Generated reset token: {reset_token}")

        send_reset_email(email, reset_token)

        return jsonify({"message": "Password reset email sent"}), 200

    except Exception as e:
        print(f"❌ Forgot Password Error: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500


@forgot_password_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """Validates token and resets password."""
    try:
        data = request.json
        token = data.get("token")
        new_password = data.get("password")

        if not token or not new_password:
            return jsonify({"message": "Token and password are required"}), 400

        try:
            decoded_token = decode_token(token)
            email = decoded_token["sub"]["email"]
        except Exception:
            return jsonify({"message": "Invalid or expired token"}), 400

        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")

        # Update password in MongoDB
        mongo.db.users.update_one(
            {"email": email},
            {"$set": {"password": hashed_password}}
        )

        return jsonify({"message": "Password reset successful"}), 200

    except Exception as e:
        print(f"❌ Reset Password Error: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
