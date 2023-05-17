from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import false as sa_false

from app.main import app, cache, db
from app.models import Post
from app.utils import build_meta, generate_slug


@app.route("/api/v1/posts/<slug>", methods=["GET"])
@cache.cached()
def get_post(slug: int):
    try:
        is_active = request.args.get("is_active", None)
        filters = [Post.slug == slug]
        if is_active is not None:
            is_active = is_active == "true"
            filters.append(
                Post.is_active if is_active else Post.is_active == sa_false()
            )
        post = Post.query.filter(*filters).first()
        result = post.to_json() if post else None
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/posts", methods=["GET"])
@cache.cached()
def get_posts():
    try:
        is_active = request.args.get("is_active", None)
        is_featured = request.args.get("is_featured", None)
        filters = []
        if is_featured is not None:
            filters.append(Post.is_featured)
        if is_active is not None:
            is_active = is_active == "true"
            filters.append(
                Post.is_active if is_active else Post.is_active == sa_false()
            )
        posts = Post.query.filter(*filters).order_by(Post.id.desc()).all()
        result = [post.to_home_json() for post in posts]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/posts", methods=["POST"])
@jwt_required()
def create_post():
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
        title = request.json.get("title", None)
        summary = request.json.get("summary", None)
        cover_image = request.json.get("coverImage", None)
        is_featured = request.json.get("isFeatured", None)
        is_active = request.json.get("isActive", None)
        content = request.json.get("content", None)

        slug = generate_slug(title)
        post_exist = Post.query.filter(Post.slug == slug).first()
        if post_exist:
            slug = generate_slug(title, with_suffix=True)

        published_date = datetime.now() if is_active else None
        post = Post(
            title=title,
            slug=slug,
            summary=summary,
            cover_image=cover_image,
            is_featured=bool(is_featured),
            is_active=bool(is_active),
            content=content,
            meta_content="",
            published_date=published_date,
        )
        db.session.add(post)
        db.session.commit()
        post.meta_content = build_meta(post)
        db.session.commit()
        cache.clear()
        return jsonify(post.to_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/posts/<post_id>", methods=["POST"])
@jwt_required()
def update_post(post_id):
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
        post = Post.query.filter(Post.id == post_id).first()
        if not post:
            return jsonify({"error": f"{post_id} doesnt exits"}), 500

        post.title = request.json.get("title", None)
        post.summary = request.json.get("summary", None)
        post.cover_image = request.json.get("coverImage", None)
        post.is_featured = request.json.get("isFeatured", None)
        post.is_active = request.json.get("isActive", None)
        post.content = request.json.get("content", None)
        post.meta_content = build_meta(post)
        db.session.commit()
        cache.clear()
        return jsonify(post.to_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
