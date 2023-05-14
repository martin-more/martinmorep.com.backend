import os

from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.main import app
from app.sdk.s3_client import S3Client
from app.utils import (
    S3_HOME_IDENTIFIER,
    S3_POST_IDENTIFIER,
    S3_SNIPPETS_IDENTIFIER,
    upload_to,
)

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "martinmorep")
CONTENT_TYPE_ALLOWED = ["image/png", "image/jpeg", "multipart/form-data"]
IDENTIFIER_MAP = {
    "home": S3_HOME_IDENTIFIER,
    "post": S3_POST_IDENTIFIER,
    "snippet": S3_SNIPPETS_IDENTIFIER,
}


@app.route("/api/v1/admin/pre_signed_url", methods=["POST"])
@jwt_required()
def generate_pre_signed_url():
    """
    Arguments:
        - filename
        - source {post, home, snippet}
    :return:
    """
    try:
        filename = request.json.get("filename", None)
        source = request.json.get("source", None) or "post"
        content_type = request.json.get("contentType", None)

        if content_type not in CONTENT_TYPE_ALLOWED:
            return jsonify({"error": f"Invalid content type {content_type}"}), 500

        identifier = IDENTIFIER_MAP.get(source)
        filename = upload_to(filename, identifier or S3_POST_IDENTIFIER)
        pre_signed_url = S3Client().create_presigned_url(
            bucket_name=S3_BUCKET_NAME, object_name=filename, content_type=content_type
        )

        return jsonify(
            {
                "filename": filename,
                "preSignedUrl": pre_signed_url,
                "url": f"https://martinmorep.s3.us-east-2.amazonaws.com/{filename}",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
