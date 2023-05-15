from flask import jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import false as sa_false

from app.main import app, cache, db
from app.models import Snippet
from app.utils import build_meta, generate_slug


@app.route("/api/v1/snippets/<slug>", methods=["GET"])
@cache.cached()
def get_snippet(slug: int):
    try:
        is_active = request.args.get("is_active", None)
        filters = [Snippet.slug == slug]
        if is_active is not None:
            is_active = is_active == "true"
            filters.append(
                Snippet.is_active if is_active else Snippet.is_active == sa_false()
            )
        snippet = Snippet.query.filter(*filters).first()
        result = snippet.to_json() if snippet else None
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/snippets", methods=["GET"])
@cache.cached()
def get_snippets():
    try:
        is_active = request.args.get("is_active", None)
        filters = []
        if is_active is not None:
            is_active = is_active == "true"
            filters.append(
                Snippet.is_active if is_active else Snippet.is_active == sa_false()
            )
        snippets = Snippet.query.filter(*filters).order_by(Snippet.id.desc()).all()
        result = [snippet.to_json() for snippet in snippets]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/snippets", methods=["POST"])
@jwt_required()
def create_snippet():
    """
    Arguments:
        - title
        - description
        - tags
        - is_active
        - order
        - content
    :return:
    """
    try:
        title = request.json.get("title", None)
        description = request.json.get("description", None)

        tags = request.json.get("tags", None) or ""
        if not isinstance(tags, list):
            tags = tags.strip().split(",") if tags else []

        is_active = request.json.get("isActive", None)
        order = request.json.get("order", None)
        content = request.json.get("content", None)

        slug = generate_slug(title)
        snippet_exist = Snippet.query.filter(Snippet.slug == slug).first()
        if snippet_exist:
            slug = generate_slug(title, with_suffix=True)

        snippet = Snippet(
            title=title,
            slug=slug,
            description=description,
            tags=tags,
            is_active=bool(is_active),
            order=order,
            content=content,
            meta_content="",
        )
        db.session.add(snippet)
        db.session.commit()
        snippet.meta_content = build_meta(snippet)
        db.session.commit()

        return jsonify(snippet.to_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/snippets/<snippet_id>", methods=["POST"])
@jwt_required()
def update_snippet(snippet_id):
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
        snippet = Snippet.query.filter(Snippet.id == snippet_id).first()
        if not snippet:
            return jsonify({"error": f"{snippet_id} doesnt exits"}), 500

        snippet.title = request.json.get("title", None)
        snippet.description = request.json.get("description", None)

        tags = request.json.get("tags", None) or ""
        if not isinstance(tags, list):
            tags = tags.strip().split(",") if tags else []

        snippet.tags = tags
        snippet.order = request.json.get("order", None)
        snippet.is_active = request.json.get("isActive", None)
        snippet.content = request.json.get("content", None)
        snippet.meta_content = build_meta(snippet)
        db.session.commit()

        return jsonify(snippet.to_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
