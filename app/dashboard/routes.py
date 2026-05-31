from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.task_model import Task

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    if not current_user.household:

        return redirect(
            url_for("household.select_household")
        )

    household = current_user.household

    members = household.members

    member_count = len(members)

    recent_tasks = Task.query.filter_by(
    household_id=current_user.household_id
    ).order_by(
      Task.id.desc()
    ).limit(5).all()

    task_count = Task.query.filter_by(
    household_id=current_user.household_id
    ).count()

    return render_template(
        "dashboard/dashboard.html",
        household=household,
        members=members,
        member_count=member_count,
        recent_tasks=recent_tasks,
        task_count=task_count
    )