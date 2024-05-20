from functools import wraps
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app import access_level_required
from users.forms import RegisterForm
from models import User
from Database_Manager.db_crud import DbManager


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')
db = DbManager()


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@access_level_required('admin')
def admin():
    return render_template('admin/admin.html', email=current_user.email)

@admin_blueprint.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if current_user.access_level != 'admin':
        flash("You do not have permission to register a new admin!")
        return(redirect(url_for('admin.admin')))

    form = RegisterForm()

    if form.validate_on_submit():
        user = db.get_user(form.email.data)
        # if the email already exists, redirect to sign up page with error message so user can try again
        if user:
            flash("Email address already exists")
            return render_template('admin/register_admin.html', form=form)

        # create a new admin
        db.add_staff(form.email.data, form.password.data,"admin")

        # sends user back to admin page
        flash("New admin user has been registered succesfully.")
        return redirect(url_for('admin.admin'))

    return render_template('admin/register_admin.html', form=form)
