from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from Database_Manager.db_crud import DbManager
from users.forms import RegisterForm
from models import User
from app import db

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')

@admin_blueprint.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if current_user.access_level != 'admin':
        flash("You do not have permission to register a new admin!")
        return(redirect(url_for('admin.admin')))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if the email already exists, redirect to sign up page with error message so user can try again
        if user:
            flash("Email address already exists")
            return render_template('users/register_admin.html', form=form)

        # create a new admin
        DbManager.add_staff(form.email.data, form.password.data)

        # sends user back to admin page
        flash("New admin user has been registered succesfully.")
        return redirect(url_for('admin.admin'))

    return render_template('users/register_staff.html', form=form)
