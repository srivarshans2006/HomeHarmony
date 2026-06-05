from app.extensions import db


class ShoppingItem(db.Model):

    __tablename__ = "shopping_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_name = db.Column(
        db.String(100),
        nullable=False
    )

    quantity = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    household_id = db.Column(
        db.Integer,
        db.ForeignKey("households.id")
    )