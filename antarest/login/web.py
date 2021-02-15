import json
from pathlib import Path
from typing import Any, Optional

from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import (  # type: ignore
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
)

from antarest.common.auth import Auth
from antarest.common.config import Config
from antarest.login.model import User, Group, Role
from antarest.login.service import LoginService


def create_login_api(service: LoginService, config: Config) -> Blueprint:
    bp = Blueprint(
        "create_login_api",
        __name__,
        template_folder=str(config["main.res"] / "templates"),
    )

    auth = Auth(config)

    @bp.route("/login", methods=["POST"])
    def login() -> Any:
        username = request.form.get("username") or request.json.get("username")
        password = request.form.get("password") or request.json.get("password")

        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        user = service.authenticate(username, password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=user.to_dict())
        resp = jsonify({"user": user.name, "access_token": access_token})
        # set_access_cookies(resp, access_token)
        return (
            resp,
            200,
        )

    @bp.route("/users", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def users_get_all() -> Any:
        return jsonify([u.to_dict() for u in service.get_all_users()])

    @bp.route("/users/<int:id>", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def users_get_id(id: int) -> Any:
        user = service.get_user(id)
        if user:
            return jsonify(user.to_dict())
        else:
            return "", 404

    @bp.route("/users", methods=["POST"])
    @auth.protected(roles=[Role.ADMIN])
    def users_create() -> Any:
        user = User.from_dict(json.loads(request.data))
        return jsonify(service.save_user(user).to_dict())

    @bp.route("/users/<int:id>", methods=["DELETE"])
    @auth.protected(roles=[Role.ADMIN])
    def users_delete(id: int) -> Any:
        service.delete_user(id)
        return jsonify(id), 200

    @bp.route("/groups", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_get_all() -> Any:
        return jsonify([g.to_dict() for g in service.get_all_groups()])

    @bp.route("/groups/<int:id>", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_get_id(id: int) -> Any:
        group = service.get_group(id)
        if group:
            return jsonify(group.to_dict())
        else:
            return f"Group {id} not found", 404

    @bp.route("/groups", methods=["POST"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_create() -> Any:
        group = Group.from_dict(json.loads(request.data))
        return jsonify(service.save_group(group).to_dict())

    @bp.route("/groups/<int:id>", methods=["DELETE"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_delete(id: int) -> Any:
        service.delete_group(id)
        return jsonify(id), 200

    @bp.route("/protected")
    @auth.protected()
    def protected() -> Any:
        return f"user id={get_jwt_identity()}"

    return bp
