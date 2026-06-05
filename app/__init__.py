from flask import Flask
from flask_login import current_user

from app.config import Config

from app.extensions import (
    db,
    migrate,
    login_manager
)

from app.auth.routes import auth_bp
from app.dashboard.routes import dashboard_bp
from app.household.routes import household_bp
from app.tasks.routes import tasks_bp
from app.expenses.routes import expenses_bp
from app.shopping.routes import shopping_bp
from app.notifications.routes import notifications_bp

from app.models.user_model import User
from app.models.household_model import Household
from app.models.task_model import Task
from app.models.expense_model import Expense
from app.models.notification_model import Notification
from app.models.user_notification_model import UserNotification
from app.settings.routes import settings_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

   

    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(household_bp)

    app.register_blueprint(tasks_bp)

    app.register_blueprint(expenses_bp)

    app.register_blueprint(shopping_bp)

    app.register_blueprint(notifications_bp)

    app.register_blueprint(settings_bp)

    @app.context_processor
    def inject_notifications():

        unread_notifications = 0

        if (
            current_user.is_authenticated
            and current_user.household_id
        ):

            notifications = Notification.query.filter_by(
                household_id=current_user.household_id
            ).all()

            for notification in notifications:

                user_notification = UserNotification.query.filter_by(
                    user_id=current_user.id,
                    notification_id=notification.id
                ).first()

                if not user_notification:

                    unread_notifications += 1

                elif (
                    not user_notification.is_read
                    and not user_notification.dismissed
                ):

                    unread_notifications += 1

        return dict(
            unread_notifications=unread_notifications
        )
    return app