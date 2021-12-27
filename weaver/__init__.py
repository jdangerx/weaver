import os

from flask import Flask, request


def create_app(test_config=None):
    app = Flask(
        __name__, instance_relative_config=True
    )  # what's instance relative config?
    dbpath = os.path.join(app.instance_path, "weaver.sqlite")

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{dbpath}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    from weaver.model import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        app.config.from_pyfile(
            "config.py", silent=True
        )  # where is this path relative to? presumably instance?
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from weaver import auth

    app.register_blueprint(auth.bp)

    return app
