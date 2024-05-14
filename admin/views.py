from flask import Blueprint, render_template, redirect, url_for

from admin.forms import RegisterForm
from models import User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def add_admin():
    form = RegisterForm
    if form.validate_on_submit():
        # The same registration logic as above, but set the access_level to 'admin'
        new_admin = User(email=form.email.data,
                         password=form.password.data,
                         access_level='admin')


    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/admin', methods=['GET','POST'])
def add_staff():
    form = RegisterForm
    if form.validate_on_submit():
        # The same registration logic as above, but set the access_level to 'admin'
        new_staff = User(email=form.email.data,
                         password=form.password.data,
                         access_level='staff')

    return redirect(url_for('admin.admin'))

# @admin_blueprint.route('/admin', methods=['POST'])
# def delete_staff():


# @admin_blueprint.route('/admin', methods=['POST'])
# def get_staff_account():
#     return render_template('users/account.html')