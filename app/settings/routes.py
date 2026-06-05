from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)



from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.extensions import db
from app.models.notification_model import Notification
from app.models.user_model import User


settings_bp = Blueprint(
    "settings",
    __name__
)
from flask_login import (
    login_required,
    current_user,
    logout_user
)

@settings_bp.route("/settings")
@login_required
def settings():

    return render_template(
        "settings/settings.html"
    )


@settings_bp.route(
    "/edit-profile",
    methods=["GET", "POST"]
)
@login_required
def edit_profile():

    if request.method == "POST":

        current_user.full_name = request.form.get(
            "full_name"
        )

        current_user.email = request.form.get(
            "email"
        )

        db.session.commit()

        return redirect(
            url_for(
                "settings.settings"
            )
        )

    return render_template(
        "settings/edit_profile.html"
    )


@settings_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form.get(
            "current_password"
        )

        new_password = request.form.get(
            "new_password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )

        if not check_password_hash(
            current_user.password,
            current_password
        ):

            return "Current password is incorrect"

        if new_password != confirm_password:

            return "Passwords do not match"

        current_user.password = (
            generate_password_hash(
                new_password
            )
        )

        db.session.commit()

        return redirect(
            url_for(
                "settings.settings"
            )
        )

    return render_template(
        "settings/change_password.html"
    )

@settings_bp.route(
    "/leave-household"
)
@login_required
def leave_household():

    household_id = current_user.household_id

    notification = Notification(

        household_id=household_id,

        message=f"{current_user.full_name} left the household"
    )

    db.session.add(notification)

    current_user.household_id = None

    db.session.commit()

    return redirect(
        url_for(
            "dashboard.dashboard"
        )
    )

@settings_bp.route("/delete-account")
@login_required
def delete_account():

    user = User.query.get(
        current_user.id
    )

    logout_user()

    db.session.delete(user)

    db.session.commit()

    return redirect(
        url_for(
            "auth.login"
        )
    )