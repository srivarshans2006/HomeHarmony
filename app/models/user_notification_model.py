from app.extensions import db


class UserNotification(db.Model):

    __tablename__ = "user_notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    notification_id = db.Column(
        db.Integer,
        db.ForeignKey("notifications.id")
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    dismissed = db.Column(
        db.Boolean,
        default=False
    )