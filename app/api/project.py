from flask import jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import false as sa_false

from app.main import app, cache, db
from app.models import Project
from app.utils import build_meta, generate_slug


@app.route("/api/v1/projects/<slug>", methods=["GET"])
@cache.cached()
def get_project(slug: int):
    try:
        is_active = request.args.get("is_active", None)
        filters = [Project.slug == slug]
        if is_active is not None:
            is_active = is_active == "true"
            filters.append(
                Project.is_active if is_active else Project.is_active == sa_false()
            )
        project = Project.query.filter(*filters).first()
        result = project.to_json() if project else None
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/projects", methods=["GET"])
@cache.cached()
def get_projects():
    try:
        is_active = request.args.get("is_active", None)
        is_featured = request.args.get("is_featured", None)
        filters = []
        if is_featured is not None:
            filters.append(Project.is_featured)
        if is_active is not None:
            is_active = is_active == "true"
            filters.append(
                Project.is_active if is_active else Project.is_active == sa_false()
            )
        projects = Project.query.filter(*filters).order_by(Project.id.desc()).all()
        result = [project.to_json() for project in projects]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/projects", methods=["POST"])
@jwt_required()
def create_project():
    """
    Arguments:
        - name
        - description
        - image
        - live_url
        - repo
        - is_active
        - is_featured
        - stacks
        - order
    :return:
    """
    try:
        name = request.json.get("name", None)
        description = request.json.get("description", None)
        image = request.json.get("image", None)
        live_url = request.json.get("liveUrl", None)
        repo = request.json.get("repo", None)

        stacks = request.json.get("stacks", None) or ""
        if not isinstance(stacks, list):
            stacks = stacks.strip().split(",") if stacks else []
        stacks = stacks

        order = request.json.get("order", None)
        content = ""
        is_featured = request.json.get("isFeatured", None)
        is_active = request.json.get("isActive", None)

        slug = generate_slug(name)
        project_exist = Project.query.filter(Project.slug == slug).first()
        if project_exist:
            slug = generate_slug(name, with_suffix=True)

        project = Project(
            name=name,
            slug=slug,
            description=description,
            image=image,
            is_featured=bool(is_featured),
            is_active=bool(is_active),
            live_url=live_url,
            repo=repo,
            stacks=stacks,
            order=order,
            content=content,
            meta_content="",
        )
        db.session.add(project)
        db.session.commit()
        project.meta_content = build_meta(project)
        db.session.commit()

        return jsonify(project.to_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/projects/<project_id>", methods=["POST"])
@jwt_required()
def update_project(project_id):
    """
    Arguments:
        - title
        - summary
        - is_featured
        - is_active
        - content
        - preview_content
    :return:
    """
    try:
        project = Project.query.filter(Project.id == project_id).first()
        if not project:
            return jsonify({"error": f"{project_id} doesnt exits"}), 500

        project.name = request.json.get("name", None)
        project.order = request.json.get("order", None)
        project.description = request.json.get("description", None)
        project.image = request.json.get("image", None)
        project.live_url = request.json.get("liveUrl", None)
        project.repo = request.json.get("repo", None)
        project.is_active = request.json.get("isActive", None)
        project.is_featured = request.json.get("isFeatured", None)

        stacks = request.json.get("stacks", None) or ""
        if not isinstance(stacks, list):
            stacks = stacks.strip().split(",") if stacks else []

        project.stacks = stacks
        project.content = request.json.get("content", None)
        project.meta_content = build_meta(project)
        db.session.commit()

        return jsonify(project.to_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
