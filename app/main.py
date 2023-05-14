import os
from datetime import timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask_sqlalchemy import SQLAlchemy

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS")

app = Flask(__name__)

# CORS
cors = CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS.split(",")}})

# JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

# SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/api/v1/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not ADMIN_USER or not ADMIN_PASSWORD:
        return jsonify({"msg": "Misconfiguration error!"}), 500
    if username != ADMIN_USER or password != ADMIN_PASSWORD:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(
        accessToken=access_token,
        refreshToken=refresh_token,
        userName=username,
    )


@app.route("/api/v1/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(accessToken=access_token)
