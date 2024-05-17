from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from users.forms import LoginForm, RegisterForm, UpdatePasswordForm
from models import User
from Database_Manager.db_crud import DbManager

users_blueprint = Blueprint('users', __name__, template_folder='templates')
db = DbManager()

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            user = db.get_user(form.email.data)

            # Checks the users credentials
            if not user or not user.password:
                flash("Invalid login")
                return render_template('users/login.html', form=form)
            else:
                # Log the user in
                login_user(user)
                # Redirect based on user role
                if current_user.access_level == 'user':
                    return redirect(url_for('users.account'))
                elif current_user.access_level == 'admin':
                    return redirect(url_for('admin.admin'))
                else:
                    # Redirect to a default page if user role is not defined
                    return redirect(url_for('main.index'))
            # Add a return statement here to handle the case when form is not submitted
        return render_template('users/login.html', form=form)
    else:
        # Displays error message
        flash("You are already logged in.")
        return redirect(url_for('main.index'))

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register_staff():
    if current_user.access_level != 'admin':
        flash("You do not have permission to register a new staff!")
        return(redirect(url_for('admin.admin')))
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register_staff.html', form=form)

        # create a new user with the form data
        db.add_staff(form.email.data,form.password.data,"user")
        return redirect(url_for('users.login'))

    return render_template('users/register_staff.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@users_blueprint.route('/update_password', methods=['GET', 'POST'])
def update_password():
    form = UpdatePasswordForm()
    # validate submitted ChangePasswordForm
    if form.validate_on_submit():
        if current_user.password != form.current_password.data:
            flash('Incorrect current password.')
            return render_template('users/update_password.html', form=form)
        if current_user.password == form.new_password.data:
            flash('New password must be different from the current password.')
            return render_template('users/update_password.html', form=form)
        db.change_password(current_user.id,current_user.password, form.new_password.data)
        flash('Password has been changed successfully.')
        return redirect(url_for('users.account'))

    return render_template('users/update_password.html', form=form)

@users_blueprint.route('/account')
@login_required
def account():
    return render_template('users/account.html',
                           user_id=current_user.user_id,
                           email=current_user.email,
                           access_level=current_user.access_level)