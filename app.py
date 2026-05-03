from flask import Config, Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import re
import routes
import os

from models import db, Admin, Opportunity

app = Flask(__name__)
app.config.from_object(Config)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = "suryamahesh039@gmail.com"
# app.config["MAIL_PASSWORD"] = "ywkd ejox ljnt xdwv"
# app.config["MAIL_DEFAULT_SENDER"] = "suryamahesh039@gmail.com"

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

ALLOWED_CATEGORIES = [
    "Technology",
    "technology",
    "Business",
    "business",
    "Design",
    "design",
    "Marketing",
    "marketing",
    "Data Science",
    "data science",
    "Other",
    "other"
]

mail = Mail(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])



@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# ---------------- CHECK SESSION ----------------
@app.route("/check-session")
def check_session():
    if current_user.is_authenticated:
        return jsonify({
            "logged_in": True,
            "email": current_user.email
        })
    return jsonify({"logged_in": False})


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    confirm = data.get("confirm_password", "").strip()

    if not name or not email or not password or not confirm:
        return jsonify({"error": "All fields required"}), 400

    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if password != confirm:
        return jsonify({"error": "Passwords do not match"}), 400

    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Account already exists"}), 400

    user = Admin(
        full_name=name,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"})


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    remember = data.get("remember", False)

    user = Admin.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user, remember=remember)
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid email or password"}), 401


# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})


# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["POST"])
def forgot():
    data = request.get_json()
    email = data.get("email", "").strip()

    user = Admin.query.filter_by(email=email).first()

    if user:
        token = serializer.dumps(email)
        reset_link = f"http://127.0.0.1:5000/reset/{token}"

        msg = Message(
            subject="Password Reset Request",
            recipients=[email]
        )

        msg.body = f"""
Hello,

Click the link below to reset your password:

{reset_link}

This link expires in 1 hour.

If you did not request this, ignore this email.
        """

        mail.send(msg)

    return jsonify({
        "message": "If account exists, reset link sent to email"
    })


# ---------------- RESET PASSWORD ----------------
@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    try:
        email = serializer.loads(token, max_age=3600)
    except:
        return "Reset link expired or invalid"

    # When link is opened in browser
    if request.method == "GET":
        return render_template("index.html")

    # When new password is submitted
    data = request.get_json()
    password = data.get("password", "").strip()

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    user = Admin.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid link"}), 400

    user.password = generate_password_hash(password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully"})

# ---------------- GET OPPORTUNITIES ----------------
@app.route("/opportunities")
@login_required
def opportunities():
    items = Opportunity.query.filter_by(admin_id=current_user.id).all()

    result = []

    for i in items:
        result.append({
            "id": i.id,
            "name": i.name,
            "duration": i.duration,
            "start_date": i.start_date,
            "description": i.description,
            "skills": i.skills,
            "category": i.category,
            "future_opportunities": i.future_opportunities,
            "max_applicants": i.max_applicants
        })

    return jsonify(result)


# ---------------- ADD OPPORTUNITY ----------------
@app.route("/add-opportunity", methods=["POST"])
@login_required
def add():
    data = request.get_json()

    required = [
        "name", "duration", "start_date",
        "description", "skills",
        "category", "future_opportunities"
    ]

    for field in required:
        if not data.get(field, "").strip():
            return jsonify({"error": f"{field} is required"}), 400

    if data["category"] not in ALLOWED_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    item = Opportunity(
        name=data["name"],
        duration=data["duration"],
        start_date=data["start_date"],
        description=data["description"],
        skills=data["skills"],
        category=data["category"],
        future_opportunities=data["future_opportunities"],
        max_applicants=data.get("max_applicants"),
        admin_id=current_user.id
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Added successfully"})


# ---------------- EDIT ----------------
@app.route("/edit/<int:id>", methods=["PUT"])
@login_required
def edit(id):
    item = Opportunity.query.get_or_404(id)

    if item.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    if data["category"] not in ALLOWED_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    item.name = data["name"]
    item.duration = data["duration"]
    item.start_date = data["start_date"]
    item.description = data["description"]
    item.skills = data["skills"]
    item.category = data["category"]
    item.future_opportunities = data["future_opportunities"]
    item.max_applicants = data["max_applicants"]

    db.session.commit()

    return jsonify({"message": "Updated"})


# ---------------- DELETE ----------------
@app.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete(id):
    item = Opportunity.query.get_or_404(id)

    if item.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)