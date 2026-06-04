from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# ======================
# Team Table
# ======================

class Team(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    team_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    users = db.relationship(
        'User',
        backref='team',
        lazy=True
    )


# ======================
# Forest Table
# ======================

class Forest(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey('team.id'),
        unique=True
    )

    water_count = db.Column(
        db.Integer,
        default=0
    )

    tree_count = db.Column(
        db.Integer,
        default=0
    )

    current_stage = db.Column(
        db.String(50),
        default="Seed"
    )


# ======================
# User Table
# ======================

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey('team.id')
    )

    water_bucket = db.Column(
        db.Integer,
        default=1
    )

    last_watered = db.Column(
        db.DateTime,
        nullable=True
    )


# ======================
# Completed Trees
# ======================

class CompletedTree(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey('team.id')
    )

    user_name = db.Column(
        db.String(100)
    )

    tree_image = db.Column(
        db.String(100)
    )