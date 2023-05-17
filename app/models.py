from datetime import datetime

from app.main import db
from app.utils import camel_case


class MarkdownableMixin:
    meta_content = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=True)
    preview_content = db.Column(db.String, nullable=True)


class Post(db.Model, MarkdownableMixin):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    summary = db.Column(db.String, nullable=True)
    cover_image = db.Column(db.String, nullable=True)
    is_featured = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    published_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )
    meta_attrs = [
        "id",
        "title",
        "slug",
        "summary",
        "cover_image",
        "is_featured",
        "is_active",
    ]

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "coverImage": self.cover_image,
            "isFeatured": self.is_featured,
            "isActive": self.is_active,
            "publishedDate": self.published_date,
            "updatedDate": self.updated_date,
            "meta": self.meta_content,
            "content": self.content,
            "previewContent": self.preview_content,
        }

    def to_home_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "coverImage": self.cover_image,
            "isFeatured": self.is_featured,
            "isActive": self.is_active,
            "publishedDate": self.published_date,
        }


class Project(db.Model, MarkdownableMixin):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    order = db.Column(db.Integer, default=0)
    description = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    live_url = db.Column(db.String, nullable=True)
    repo = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean(), default=False)
    is_featured = db.Column(db.Boolean(), default=False)
    stacks = db.Column(db.ARRAY(db.String), nullable=True)

    meta_attrs = [
        "id",
        "name",
        "slug",
        "order",
        "description",
        "image",
        "live_url",
        "repo",
        "is_active",
        "is_featured",
        "stacks",
    ]

    def to_json(self, attrs=None):
        if attrs:
            _json = {}
            for attr in attrs:
                _json[camel_case(attr)] = getattr(self, attr)
                return _json
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "order": self.order,
            "description": self.description,
            "image": self.image,
            "liveUrl": self.live_url,
            "repo": self.repo,
            "isFeatured": self.is_featured,
            "isActive": self.is_active,
            "stacks": self.stacks,
            "meta": self.meta_content,
            "content": self.content,
            "previewContent": self.preview_content,
        }


class Snippet(db.Model, MarkdownableMixin):
    __tablename__ = "snippet"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    tags = db.Column(db.ARRAY(db.String), nullable=True)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean(), default=False)

    meta_attrs = [
        "id",
        "title",
        "slug",
        "description",
        "tags",
        "order",
        "is_active",
    ]

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "tags": self.tags,
            "order": self.order,
            "isActive": self.is_active,
            "meta": self.meta_content,
            "content": self.content,
            "previewContent": self.preview_content,
        }
