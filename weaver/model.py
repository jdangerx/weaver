import hashlib

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, unique=False, nullable=False)
    # For superuser/mod etc.
    group = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, plaintext):
        self.password = generate_password_hash(plaintext, "pbkdf2:sha256:500000")

    def check_password(self, plaintext):
        return check_password_hash(self.password, plaintext)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("posts", lazy=True))
    parent = db.Column(db.String, nullable=True, unique=True)
    digest = db.Column(db.String, nullable=False, unique=True)
    body = db.Column(db.String, nullable=False, unique=True)
    created = db.Column(db.DateTime, default=db.func.now())

    def make_digest(self):
        message = f"a:{self.author.id}p:{self.parent}b:{self.body}"
        md5 = hashlib.md5(message.encode("utf-8"))
        self.digest = md5.hexdigest()

    def __repr__(self):
        return f"<Post by {self.author} at {self.created.isoformat()}>"
