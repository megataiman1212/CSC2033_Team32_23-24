from flask import Blueprint, render_template, redirect, url_for, get_flashed_messages

from Database_Manager.db_crud import DbManager
from admin.forms import RegisterForm
from flask_login import login_required

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    form = RegisterForm
    if form.validate_on_submit():
        DbManager.add_staff(RegisterForm.email.data, RegisterForm.password.data, "admin")

    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    form = RegisterForm
    if form.validate_on_submit():
        DbManager.add_staff(form.email.data, form.password.data, "staff")

    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/delete_staff', methods=['POST'])
def delete_staff():

    DbManager.delete_staff()

    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/get_staff_account', methods=['POST'])
def get_staff_account():
    accounts = DbManager.get_all_users()

    return render_template('admin/account.html', accounts=accounts)





