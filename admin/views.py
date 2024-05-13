from flask import Blueprint, render_template

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')
