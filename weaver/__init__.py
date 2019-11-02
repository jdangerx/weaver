import os

from flask import Flask, jsonify, render_template, redirect, url_for, flash
from flask_login import (
    current_user,
    login_user,
    login_required,
    LoginManager,
    logout_user,
)
from weaver.model import db, migrate, User, Post
from weaver.forms import LoginForm, PostForm


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    login_manager = LoginManager(app)
    db_url = os.getenv("DATABASE_URL", "postgresql://localhost/weaver")
    secret_key = os.getenv("WV_SECRET_KEY", "dev")

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/", methods=["GET"])
    def index():
        if current_user.is_authenticated:
            return render_template("index.html", posts=Post.query.all())
        else:
            return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("invalid login!")
                return redirect(url_for("login"))
            login_user(user)
            return redirect(url_for("index"))
        return render_template("login.html", form=form)

    @app.route("/logout", methods=["GET"])
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/post/<reply_to>", methods=["GET", "POST"])
    @login_required
    def submit_post(reply_to):
        form = PostForm()
        if form.validate_on_submit():
            new_post = Post(body=form.body.data, parent=reply_to)
            new_post.author = current_user
            new_post.make_digest()
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("post.html", form=form)

    @app.route("/api/posts/all", methods=["GET"])
    @login_required
    def posts():
        all_posts = [
            {
                "author": p.author.username,
                "parent": p.parent,
                "body": p.body,
                "created": p.created,
            }
            for p in Post.query.all()
        ]
        return jsonify(all_posts)

    @app.route("/api/posts", methods=["POST"])
    @login_required
    def create_post():
        if "body" not in post_params:
            return "Missing 'body' field in JSON.", 400
        new_post = Post(**request.json)
        new_post.author = current_user
        new_post.make_digest()
        db.session.add(new_post)
        db.session.commit()

    db.init_app(app)
    migrate.init_app(app, db)

    return app
