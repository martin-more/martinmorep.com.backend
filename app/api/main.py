from flask import jsonify

from app.main import app
from app.models import Post, Project


@app.route("/api/v1/home", methods=["GET"])
def get_home_stuff():
    try:
        posts = (
            Post.query.filter(Post.is_featured, Post.is_active)
            .order_by(Post.id.desc())
            .all()
        )
        posts = [post.to_json() for post in posts]
        projects = (
            Project.query.filter(Project.is_featured, Project.is_active)
            .order_by(Project.id.desc())
            .all()
        )
        projects = [project.to_json() for project in projects]
        return jsonify({"posts": posts, "projects": projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
