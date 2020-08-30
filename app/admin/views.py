"""
This is place for all admin views.
Views should ALWAYS extend ProtectedModelView !
"""
from flask import url_for, request, abort, flash
from flask_admin import BaseView, AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView as _ModelView
from flask_admin.form import SecureForm
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from app.admin.forms import LoginForm, ChangePasswordForm
from app.extensions import db, admin
from app.models.customer import Customer
from app.models.reservation import Reservation


class ProtectedBaseView(BaseView):

    def is_accessible(self):
        """ All admin views require authentication """
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        """
        Redirect to login page if user doesn't have access
        """
        return redirect(url_for('admin.login_view', next=request.url))

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('admin.login_view', next=request.url))


class ProtectedModelView(_ModelView, ProtectedBaseView):
    """ Secured Model View """
    form_base_class = SecureForm


class ProtectedIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        """ Render the welcome page for the admin """
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(ProtectedIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        """ Logic to handle a user logging in """
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user:
                login_user(user)
            else:
                flash("Invalid Credentials")

        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(ProtectedIndexView, self).index()

    @expose('/password/', methods=('GET', 'POST'))
    def change_password_view(self):
        """ Logic for updating a password """
        if not current_user.is_authenticated:
            abort(403)

        form = ChangePasswordForm(request.form)
        if helpers.validate_form_on_submit(form):
            current_user.set_password(form.new_password.data)
            db.session.add(current_user)
            db.session.commit()
            logout_user()
            flash("Password updated successfully. Please login again.", "success")
            return redirect(url_for('.login_view'))

        self._template_args['form'] = form
        return self.render('admin/password.html')

    @expose('/logout/')
    def logout_view(self):
        """ Logout """
        logout_user()
        return redirect(url_for('.index'))


class CustomerListView(ProtectedModelView):
    """ Customers are only listed and can be edited but not created """
    form_excluded_columns = ['registered_on', 'reservations']
    column_list = ['id', 'first_name', 'last_name', 'street', 'zip_code', 'city', 'tel', 'email']

    column_editable_list = ['first_name', 'last_name', 'street', 'zip_code', 'city', 'tel', 'email']


class ReservationListView(ProtectedModelView):
    form_excluded_columns = ['timestamp']

    column_editable_list = ['confirmed', ]


# Register ModelViews

admin.add_view(CustomerListView(Customer, db.session, name="Kunden"))  # Customer
admin.add_view(ReservationListView(Reservation, db.session, name="Reservierungen"))  # Customer
