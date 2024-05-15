from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, login_required
from users.forms import LoginForm
from models import User

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            # Checks the users credentials
            if not user or not user.password:
                flash("Invalid login")
                return render_template('users/login.html', form=form)


            else:
                # Log the user in
                login_user(user)
                return redirect(url_for('admin.admin'))

                # Redirects the user depending on their role
        #return render_template('users/login.html', form=form)
    else:
        # Displays error message
        flash("You are already logged in")
        return render_template('main/index.html')


@users_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    # create password form object
    form = PasswordForm()

    if form.validate_on_submit():
        # if current password match with the password in the database
        # if new password not same as current password in the database

        if current_user.password == form.current_password.data and form.new_password.data != current_user.password:
            # update the password and commit in the database
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Password changed successfully', 'success')

        else:
            # password is not changed
            flash('Password is not changed successfully.Please try again')


    return render_template('users/update_password.html', form=form)
