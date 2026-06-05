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

from app.models.shopping_model import ShoppingItem

from app.models.notification_model import Notification

shopping_bp = Blueprint(
    "shopping",
    __name__
)


@shopping_bp.route("/shopping")
@login_required
def shopping_list():

    items = ShoppingItem.query.filter_by(
        household_id=current_user.household_id
    ).all()

    return render_template(
        "shopping/shopping_list.html",
        items=items
    )


@shopping_bp.route(
    "/create-shopping",
    methods=["GET", "POST"]
)
@login_required
def create_shopping():

    if request.method == "POST":

        item_name = request.form.get(
            "item_name"
        )

        quantity = request.form.get(
            "quantity"
        )

        item = ShoppingItem(

            item_name=item_name,

            quantity=quantity,

            household_id=current_user.household_id
        )

        db.session.add(item)

        notification = Notification(

            household_id=current_user.household_id,

            message=f"{current_user.full_name} added shopping item '{item.item_name}'"
        )

        db.session.add(notification)

        db.session.commit()

        return redirect(
            url_for("shopping.shopping_list")
        )

    return render_template(
        "shopping/create_shopping.html"
    )

@shopping_bp.route(
    "/update-shopping-status/<int:item_id>",
    methods=["POST"]
)
@login_required
def update_shopping_status(item_id):

    item = ShoppingItem.query.filter_by(
        id=item_id,
        household_id=current_user.household_id
    ).first()

    if not item:

        return "Item not found"

    item.status = request.form.get(
        "status"
    )

    db.session.commit()

    return redirect(
        url_for("shopping.shopping_list")
    )

@shopping_bp.route(
    "/delete-shopping/<int:item_id>"
)
@login_required
def delete_shopping(item_id):

    item = ShoppingItem.query.filter_by(
        id=item_id,
        household_id=current_user.household_id
    ).first()

    if not item:

        return "Item not found"

    db.session.delete(item)

    db.session.commit()

    return redirect(
        url_for("shopping.shopping_list")
    )

@shopping_bp.route(
    "/edit-shopping/<int:item_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_shopping(item_id):

    item = ShoppingItem.query.filter_by(
        id=item_id,
        household_id=current_user.household_id
    ).first()

    if not item:

        return "Item not found"

    if request.method == "POST":

        item.item_name = request.form.get(
            "item_name"
        )

        item.quantity = request.form.get(
            "quantity"
        )

        db.session.commit()

        return redirect(
            url_for("shopping.shopping_list")
        )

    return render_template(
        "shopping/edit_shopping.html",
        item=item
    )