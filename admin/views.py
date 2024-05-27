from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from users.forms import RegisterForm
from Database_Manager.db_crud import DbManager
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')
db = DbManager()


@admin_blueprint.route('/admin/admin', methods=['GET', 'POST'])
def admin():
    """
    Checks permission is correct and then sends to admin page
    :return: admin.html
    :return: Error403.html
    """

    if current_user.access_level == 'admin':
        return render_template('admin/admin.html')
    else:
        return render_template('Error403.html')


@admin_blueprint.route('/<string:role>/add_staff', methods=['GET', 'POST'])
def add_staff(role):
    """
    Adds new staff to the database
    :param role: role of new staff (admin/ user)
    :return: add_staff.html
    """

    if current_user.access_level != 'admin':
        flash("You do not have permission to register a new admin!")
        return redirect(url_for('admin.admin'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = db.get_user(form.email.data)
        # if the email already exists, redirect to sign up page with error message so user can try again
        if user:
            flash("Email address already exists")
            return render_template('admin/add_staff.html', form=form)

        # create a new admin
        db.add_staff(form.email.data, form.password.data, role)

        # sends user back to admin page
        flash("New admin user has been registered successfully.")
        return redirect(url_for('admin.admin'))

    return render_template('admin/add_staff.html', form=form)
