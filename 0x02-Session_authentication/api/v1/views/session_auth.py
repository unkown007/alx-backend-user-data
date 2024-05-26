#!/usr/bin/env python3
""" Module to handle all routes for Session authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> str:
    """ Session authentication login
    """
    if not request.form.get("email") or len(request.form.get("email")) == 0:
        return jsonify({"error": "email missing"}), 400

    if not request.form.get("password") or \
            len(request.form.get("password")) == 0:
        return jsonify({"error": "password missing"}), 400

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.search({"email": email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user[0].to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route(
    "/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """ Log out a user by removing his session
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
