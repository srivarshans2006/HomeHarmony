from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from app.models.notification_model import Notification
from app.models.user_notification_model import UserNotification


notifications_bp = Blueprint(
    "notifications",
    __name__
)


@notifications_bp.route("/notifications")
@login_required
def notification_list():

    notifications = Notification.query.filter_by(
        household_id=current_user.household_id
    ).order_by(
        Notification.id.desc()
    ).all()

    visible_notifications = []

    for notification in notifications:

        user_notification = UserNotification.query.filter_by(
            user_id=current_user.id,
            notification_id=notification.id
        ).first()

        if not user_notification:

            user_notification = UserNotification(
                user_id=current_user.id,
                notification_id=notification.id,
                is_read=True,
                dismissed=False
            )

            db.session.add(user_notification)

        else:

            user_notification.is_read = True

        if not user_notification.dismissed:

            visible_notifications.append(
                notification
            )

    db.session.commit()

    return render_template(
        "notifications/notification_list.html",
        notifications=visible_notifications
    )


@notifications_bp.route(
    "/dismiss-notification/<int:notification_id>"
)
@login_required
def dismiss_notification(notification_id):

    existing = UserNotification.query.filter_by(
        user_id=current_user.id,
        notification_id=notification_id
    ).first()

    if not existing:

        existing = UserNotification(
            user_id=current_user.id,
            notification_id=notification_id,
            is_read=True,
            dismissed=True
        )

        db.session.add(existing)

    else:

        existing.dismissed = True

    db.session.commit()

    return redirect(
        url_for(
            "notifications.notification_list"
        )
    )

@notifications_bp.route(
    "/clear-notifications"
)
@login_required
def clear_notifications():

    notifications = Notification.query.filter_by(
        household_id=current_user.household_id
    ).all()

    for notification in notifications:

        existing = UserNotification.query.filter_by(
            user_id=current_user.id,
            notification_id=notification.id
        ).first()

        if not existing:

            existing = UserNotification(
                user_id=current_user.id,
                notification_id=notification.id,
                is_read=True,
                dismissed=True
            )

            db.session.add(existing)

        else:

            existing.dismissed = True

    db.session.commit()

    return redirect(
        url_for(
            "notifications.notification_list"
        )
    )