import uuid
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from app.models.household_model import Household


household_bp = Blueprint(
    "household",
    __name__
)

@household_bp.route(
    "/join-household",
    methods=["GET", "POST"]
)
@login_required
def join_household():

    if request.method == "POST":

        invite_code = request.form.get(
            "invite_code"
        )

        household = Household.query.filter_by(
            invite_code=invite_code
        ).first()

        if not household:

            return "Invalid invite code"

        current_user.household_id = household.id

        db.session.commit()

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(
        "household/join_household.html"
    )
@household_bp.route(
    "/create-household",
    methods=["GET", "POST"]
)
@login_required
def create_household():

    if request.method == "POST":

        household_name = request.form.get(
            "household_name"
        )

        invite_code = (
            "HOME-" +
            str(uuid.uuid4())[:6].upper()
        )

        new_household = Household(
            household_name=household_name,
            invite_code=invite_code
        )

        db.session.add(new_household)

        db.session.commit()

        current_user.household_id = new_household.id

        db.session.commit()

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(
        "household/create_household.html"
    )

@household_bp.route("/select-household")
@login_required
def select_household():

    return render_template(
        "household/select_household.html"
    )