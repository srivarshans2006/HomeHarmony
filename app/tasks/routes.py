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

from app.models.task_model import Task

from app.models.user_model import User

from app.models.notification_model import Notification


tasks_bp = Blueprint(
    "tasks",
    __name__
)


@tasks_bp.route(
    "/create-task",
    methods=["GET", "POST"]
)
@login_required
def create_task():

    members = current_user.household.members

    if request.method == "POST":

        title = request.form.get(
            "title"
        )

        description = request.form.get(
            "description"
        )

        assigned_to = request.form.get(
            "assigned_to"
        )

        priority = request.form.get(
            "priority"
        )

        member = User.query.filter_by(
            id=assigned_to,
            household_id=current_user.household_id
        ).first()

        if not member:

            return "Invalid household member"

        task = Task(
            title=title,
            description=description,
            assigned_to=member.id,
            household_id=current_user.household_id,
            priority=priority
        )

        db.session.add(task)

        # Create a notification for the assigned user
        notification = Notification(
            message=f"{current_user.full_name} created task '{title}'",
            household_id=current_user.household_id
        )
        db.session.add(notification)

        db.session.commit()

        return redirect(
           url_for("tasks.task_list")
       )

    return render_template(
    "tasks/create_task.html",
    members=members,
    household=current_user.household
   )



@tasks_bp.route(
    "/edit-task/<int:task_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        household_id=current_user.household_id
    ).first()

    if not task:
        return "Task not found"

    members = current_user.household.members

    if request.method == "POST":

        task.title = request.form.get("title")

        task.description = request.form.get("description")

        task.priority = request.form.get("priority")

        task.assigned_to = request.form.get("assigned_to")

        db.session.commit()

        return redirect(
            url_for("tasks.task_list")
        )

    return render_template(
        "tasks/edit_task.html",
        task=task,
        members=members
    )




@tasks_bp.route("/tasks")
@login_required
def task_list():

    tasks = Task.query.filter_by(
        household_id=current_user.household_id
    ).all()

    return render_template(
        "tasks/task_list.html",
        tasks=tasks
    )

@tasks_bp.route(
    "/update-task-status/<int:task_id>",
    methods=["POST"]
)
@login_required
def update_task_status(
    task_id
):

    task = Task.query.filter_by(
        id=task_id,
        household_id=current_user.household_id
    ).first()

    if not task:

        return "Task not found"

    task.status = request.form.get(
        "status"
    )

    db.session.commit()

    return redirect(
    request.referrer or
    url_for("tasks.task_list")
)




@tasks_bp.route(
    "/delete-task/<int:task_id>"
)
@login_required
def delete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        household_id=current_user.household_id
    ).first()

    if not task:

        return "Task not found"

    db.session.delete(task)

    db.session.commit()

    return redirect(
        url_for("tasks.task_list")
    )