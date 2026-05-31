from flask import Flask
from app.config import Config
from app.extensions import db, migrate, login_manager, socketio
from app.auth.routes import auth_bp
from app.models.user_model import User
from app.dashboard.routes import dashboard_bp
from app.models.household_model import Household
from app.household.routes import household_bp
from app.models.task_model import Task
from app.tasks.routes import tasks_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    socketio.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(household_bp)
    app.register_blueprint(tasks_bp)

    
    return app