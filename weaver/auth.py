import base64

from flask import (
    Blueprint,
    current_app,
    flash,
    request,
    redirect,
    render_template,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from weaver.model import db, User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        if not password:
            error = "Password is required."

        if error is None:
            user = User(
                username=username,
                password=generate_password_hash(password),
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = User.query.filter(User.username == username).first()

        if not user:
            error = f"User {username} not found."
        elif not check_password_hash(user.password, password):
            error = f"Wrong password."

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            g.user = user
