"""
create tables post project snippet
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE "post" (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            slug VARCHAR NOT NULL,
            summary VARCHAR NULL,
            cover_image VARCHAR NULL,
            is_featured BOOL NOT NULL DEFAULT FALSE,
            is_active BOOL NOT NULL DEFAULT FALSE,
            meta_content VARCHAR NOT NULL,
            content VARCHAR NULL,
            preview_content VARCHAR NULL,
            published_date TIMESTAMP with TIME ZONE NULL,
            updated_date TIMESTAMP with TIME ZONE NULL
        );
        """,
        """
        DROP TABLE "post";
        """,
    ),
    step(
        """
        CREATE TABLE "project" (
            id SERIAL PRIMARY KEY,

            "name" VARCHAR NOT NULL,
            slug VARCHAR NOT NULL,
            "order" INTEGER NOT NULL DEFAULT 0,
            description VARCHAR NULL,
            image VARCHAR NULL,
            live_url VARCHAR NULL,
            repo VARCHAR NULL,
            is_active BOOL NOT NULL DEFAULT FALSE,
            is_featured BOOL NOT NULL DEFAULT FALSE,
            stacks VARCHAR ARRAY NULL,
            meta_content VARCHAR NOT NULL,
            content VARCHAR NULL,
            preview_content VARCHAR NULL
        );
        """,
        """
        DROP TABLE "project";
        """,
    ),
    step(
        """
        CREATE TABLE "snippet" (
            id SERIAL PRIMARY KEY,

            title VARCHAR NOT NULL,
            slug VARCHAR NOT NULL,
            description VARCHAR NULL,
            tags VARCHAR ARRAY NULL,
            "order" INTEGER NOT NULL DEFAULT 0,
            is_active BOOL NOT NULL DEFAULT FALSE,
            meta_content VARCHAR NOT NULL,
            content VARCHAR NULL,
            preview_content VARCHAR NULL
        );
        """,
        """
        DROP TABLE "snippet";
        """,
    ),
]
