from flask import Blueprint, render_template, request, redirect

database_blueprint = Blueprint('database', __name__, template_folder='templates')

@database_blueprint.route('/database', methods=['GET', 'POST'])
def admin():
    return render_template('database/database.html')