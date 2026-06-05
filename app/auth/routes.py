from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db

from app.models.user_model import User

from flask_login import (
    login_user,
    logout_user
)

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/")
def home():

    return render_template(
        "auth/login.html"
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            return render_template(
                "auth/login.html",
                error="User not found"
            )

        if not check_password_hash(
            user.password,
            password
        ):

            return render_template(
                "auth/login.html",
                error="Incorrect password"
            )

        login_user(
            user
        )

        return redirect(
            url_for(
                "dashboard.dashboard"
            )
        )

    return render_template(
        "auth/login.html",
        success=request.args.get("success")
    )


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return render_template(
                "auth/register.html",
                error="Email already registered"
            )

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password
        )

        db.session.add(
            new_user
        )

        db.session.commit()

        return redirect(
            url_for(
                "auth.login",
                success="Account created successfully. Please log in."
            )
        )

    return render_template(
        "auth/register.html"
    )


@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for(
            "auth.login"
        )
    )