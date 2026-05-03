from flask import render_template, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from app import app, mail
from config import config
from models import db, Admin, Opportunity

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


