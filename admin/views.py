from flask import Blueprint, render_template

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def add_admin():
    # form = RegisterForm
    if form.validate_on_submit():
        # The same registration logic as above, but set the role to 'admin'
        new_admin = User(email=form.email.data,
                         password=form.password.data,
                         role='admin')


    return redirect(url_for('admin.admin'))

