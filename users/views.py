from flask import Blueprint, render_template

users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('users/register.html')

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('users/login.html')

@users_blueprint.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('users/account.html')


