from flask.cli import FlaskGroup

from app.main import app

cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
