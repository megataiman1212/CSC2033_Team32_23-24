from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user
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
            if not user or not user.verify_password(form.password.data):
                return render_template('users/login.html', form=form)

            else:
                # Log the user in
                login_user(user)
                return redirect(url_for('admin.admin'))

                # Redirects the user depending on their role
        return render_template('users/login.html', form=form)
    else:
        # Displays error message
        flash("You are already logged in")
        return render_template('main/index.html')
