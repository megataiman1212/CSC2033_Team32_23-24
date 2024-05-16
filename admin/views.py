from flask import Blueprint, render_template, redirect, url_for, get_flashed_messages

import databaseControl
from admin.forms import RegisterForm
from app import db
from models import User
from flask_login import current_user

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    form = RegisterForm
    if form.validate_on_submit():
        # The same registration logic as above, but set the access_level to 'admin'
        new_admin = User(email=form.email.data,
                         password=form.password.data,
                         access_level='admin')
        # add and commit new admin to the database
        db.session.add(new_admin)
        db.session.commit()

    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/add_staff', methods=['GET','POST'])
def add_staff():
    form = RegisterForm
    if form.validate_on_submit():
        databaseControl.add_staff(form.email.data, form.password.data)

    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/delete_staff', methods=['POST'])
def delete_staff():

    databaseControl.delete_staff()

    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/get_staff_account', methods=['POST'])
def get_staff_account():
    accounts = databaseControl.get_all_users()

    return render_template('admin/account.html', accounts=accounts)





