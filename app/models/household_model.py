from app.extensions import db


class Household(db.Model):

    __tablename__ = "households"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    household_name = db.Column(
        db.String(120),
        nullable=False
    )

    invite_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    members = db.relationship(
    "User",
    backref="household",
    lazy=True
    )

    shopping_items = db.relationship(
    "ShoppingItem",
    backref="household",
    lazy=True
)
    
notifications = db.relationship(
    "Notification",
    backref="household",
    lazy=True
)
    