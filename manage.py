from flask.cli import FlaskGroup

from app.main import app, cache

cli = FlaskGroup(app)


@cli.command("clear_cache")
def create_db():
    cache.clear()


if __name__ == "__main__":
    cli()
