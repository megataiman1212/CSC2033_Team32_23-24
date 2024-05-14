from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from users.forms import LoginForm, RegisterForm
from models import User
from app import db

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

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)


        # create a new user with the form data
        new_user = User(email=form.email.data,
                        password=form.password.data,
                        access_level='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
