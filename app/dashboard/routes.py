from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.task_model import Task
from app.models.expense_model import Expense
from app.models.notification_model import Notification
from app.models.shopping_model import ShoppingItem

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    household = current_user.household
   

    if not household:

        return render_template(
            "dashboard/no_household.html"
        )

    members = household.members

    member_count = len(members)

    tasks = Task.query.filter_by(
        household_id=household.id
    ).all()

    expenses = Expense.query.filter_by(
        household_id=household.id
    ).all()

    total_tasks = len(tasks)

    total_expenses = sum(
        expense.amount
        for expense in expenses
    )

    recent_tasks = Task.query.filter_by(
        household_id=household.id
    ).order_by(
        Task.id.desc()
    ).limit(5).all()

    recent_expenses = Expense.query.filter_by(
        household_id=household.id
    ).order_by(
        Expense.id.desc()
    ).limit(5).all()

    shopping_items = ShoppingItem.query.filter_by(
    household_id=household.id
    ).all()

    shopping_count = ShoppingItem.query.filter_by(
    household_id=household.id,
    status="Pending"
    ).count()

    return render_template(
        "dashboard/dashboard.html",

        household=household,

        members=members,

        member_count=member_count,

        total_tasks=total_tasks,

        total_expenses=total_expenses,

        recent_tasks=recent_tasks,

        recent_expenses=recent_expenses,

        shopping_count=shopping_count

        
    )