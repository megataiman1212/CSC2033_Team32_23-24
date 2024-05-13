from flask import Blueprint, render_template
from flask_login import login_required, current_user

database_blueprint = Blueprint('database', __name__, template_folder='templates')

@database_blueprint.route('/database', methods=['GET', 'POST'])
@login_required
def database():
    return render_template('database/database.html')