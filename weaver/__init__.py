import os

from flask import Flask, jsonify

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    @app.route("/posts", methods=["GET"])
    def posts():
        from datetime import datetime as dt
        import hashlib
        root = {"id": 0}
        hash_template = "a:{author}p:{parent}b:{body}t:{timestamp}"
        loomings = {
            "author": "herman",
            "parent": None,
            "body": "# Moby Dick\n\n##Chapter 1. Loomings\n\nI'm Ishmael",
            "timestamp": "2019-10-29T08:02:00-04:00"
        }
        md5 = hashlib.md5(hash_template.format(**loomings).encode("utf-8"))
        loomings["md5"] = md5.hexdigest()
        ishmael = {
            "author": "ishmael",
            "parent": loomings["md5"],
            "body": "'Call me Ishmael', maybe?",
            "timestamp": "2019-10-29T08:02:01-04:00"
        }
        md5 = hashlib.md5(hash_template.format(**ishmael).encode("utf-8"))
        ishmael["md5"] = md5.hexdigest()
        return jsonify([loomings, ishmael])

    return app