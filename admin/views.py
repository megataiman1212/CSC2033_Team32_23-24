from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from Database_Manager.db_crud import DbManager, UserNotFoundError
from app import access_level_required
from users.forms import RegisterForm

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin/admin', methods=['GET', 'POST'])
@login_required
@access_level_required('admin')
def admin():
    """
    Checks permission is correct and then sends to admin page
    :return: admin.html
    :return: Error403.html
    """
    db = DbManager()
    return render_template('admin/admin.html', email=current_user.email, current_users=db.get_all_users())


@admin_blueprint.route("/<string:email>/delete_user", methods=['GET', 'POST'])
@login_required
@access_level_required('admin')
def delete_user(email):
    """
    Delete user from the database
    :param email: email of the user
    :return: admin.html
    """
    db = DbManager()

    if email.upper() == current_user.email.upper():
        return render_template('admin/admin.html', email=current_user.email, current_users=db.get_all_users(),
                               message="You Cannot Delete Yourself")
    else:
        db.delete_staff(email)
        return render_template('admin/admin.html', email=current_user.email, current_users=db.get_all_users())


@admin_blueprint.route('/<string:role>/add_staff', methods=['GET', 'POST'])
@login_required
@access_level_required('admin')
def add_staff(role):
    """
    Adds new staff to the database
    :param role: role of new staff (admin/ user)
    :return: add_staff.html
    """
    db = DbManager()

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = db.get_user(form.email.data)
        except UserNotFoundError as e:
            # create a new admin
            db.add_staff(form.email.data, form.password.data, role)

            # sends user back to admin page
            # flash("New admin user has been registered successfully.")
            return redirect(url_for('admin.admin'))
        # if the email already exists, redirect to sign up page with error message so user can try again
        flash("Email address already exists")
        return render_template('admin/add_staff.html', form=form)

    return render_template('admin/add_staff.html', form=form)
