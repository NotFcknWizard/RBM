from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from models import db, Registration

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

class AdminRegistrationView(AdminModelView):
    column_list = ["id", "user.username", "event_name", "status"]
    column_labels = {"user.username": "Користувач", "event_name": "Подія", "status": "Статус"}

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

class UserRegistrationView(AdminModelView):
    column_list = ["id", "event_name", "status"]
    column_labels = {"event_name": "Подія", "status": "Статус"}

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "user"

    def get_query(self):
        return super().get_query().filter_by(user_id=current_user.id)

    def get_count_query(self):
        return super().get_count_query().filter_by(user_id=current_user.id)

def init_admin(app):
    admin = Admin(app, name="Волейбольний сайт", template_mode="bootstrap3")
    admin.add_view(AdminRegistrationView(Registration, db.session, name="Усі реєстрації", endpoint="admin_registrations"))
    admin.add_view(UserRegistrationView(Registration, db.session, name="Мої реєстрації", endpoint="user_registrations"))
