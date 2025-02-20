import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "honourkorkmaz@gmail.com"
SMTP_PASSWORD = "xwtowqqocdprpxhm"

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Secure the connection
    server.login(SMTP_USERNAME, SMTP_PASSWORD)  # Attempt login
    print("✅ SMTP Authentication Successful")
    server.quit()
except Exception as e:
    print(f"❌ SMTP Error: {e}")
