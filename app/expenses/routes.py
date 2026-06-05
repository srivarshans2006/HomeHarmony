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

from app.models.expense_model import Expense
from app.models.notification_model import Notification

expenses_bp = Blueprint(
    "expenses",
    __name__
)


@expenses_bp.route(
    "/create-expense",
    methods=["GET", "POST"]
)
@login_required
def create_expense():

    members = current_user.household.members

    if request.method == "POST":

        expense = Expense(
            title=request.form.get("title"),
            amount=request.form.get("amount"),
            category=request.form.get("category"),
            description=request.form.get("description"),
            paid_by=request.form.get("paid_by"),
            household_id=current_user.household_id
        )

        db.session.add(expense)

        notification = Notification(

            household_id=current_user.household_id,

            message=f"{current_user.full_name} added expense '{expense.title}'"
        )

        db.session.add(notification)

        db.session.commit()

        return redirect(
            url_for("expenses.expense_list")
        )

    return render_template(
        "expenses/create_expense.html",
        members=members
    )


@expenses_bp.route(
    "/edit-expense/<int:expense_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        household_id=current_user.household_id
    ).first()

    if not expense:

        return "Expense not found"

    members = current_user.household.members

    if request.method == "POST":

        expense.title = request.form.get(
            "title"
        )

        expense.amount = request.form.get(
            "amount"
        )

        expense.category = request.form.get(
            "category"
        )

        expense.paid_by = request.form.get(
            "paid_by"
        )

        expense.description = request.form.get(
            "description"
        )

        db.session.commit()

        return redirect(
            url_for("expenses.expense_list")
        )

    return render_template(
        "expenses/edit_expense.html",
        expense=expense,
        members=members
    )


@expenses_bp.route("/expenses")
@login_required
def expense_list():

    expenses = Expense.query.filter_by(
        household_id=current_user.household_id
    ).all()

    return render_template(
        "expenses/expense_list.html",
        expenses=expenses
    )

@expenses_bp.route(
    "/delete-expense/<int:expense_id>"
)
@login_required
def delete_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        household_id=current_user.household_id
    ).first()

    if not expense:

        return "Expense not found"

    db.session.delete(expense)

    db.session.commit()

    return redirect(
        url_for("expenses.expense_list")
    )