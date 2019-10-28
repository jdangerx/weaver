import os

from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, world!"

    return app
