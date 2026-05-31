from app.extensions import db


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    household_id = db.Column(
        db.Integer,
        db.ForeignKey("households.id"),
        nullable=False
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    priority = db.Column(
    db.String(20),
    default="Medium"
)