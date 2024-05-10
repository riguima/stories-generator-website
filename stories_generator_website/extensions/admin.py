from flask import redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from stories_generator_website.database import Session
from stories_generator_website.models import Product, Configuration


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


def init_app(app):
    admin = Admin(app, name='admin')
    session = Session()
    admin.add_view(AdminModelView(Product, session))
    admin.add_view(AdminModelView(Configuration, session))
