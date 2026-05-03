class config:
    SECRET_KEY = "qatar_foundation_secure_2026"

    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    MAIL_USERNAME = "suryamahesh039@gmail.com"
    MAIL_PASSWORD = "ywkd ejox ljnt xdwv"
    MAIL_DEFAULT_SENDER = "suryamahesh039@gmail.com"

    ALLOWED_CATEGORIES = [
    "Technology",
    "Business",
    "Design",
    "Marketing",
    "Data Science",
    "Other"
    ]