from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, unique=False, nullable=False)
    group = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("posts", lazy=True))
    parent = db.Column(db.String, nullable=True, unique=True)
    digest = db.Column(db.String, nullable=False, unique=True)
    body = db.Column(db.String, nullable=False, unique=True)
    created = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Post by {self.author} at {self.created.isoformat()}>"
