from flask import request
from Database_Manager.db_crud import DbManager, ProductNotFoundError
from flask import Blueprint, render_template
from flask_login import login_required
from app import access_level_required
from database.forms import ProductForm, RequiredStockForm

database_blueprint = Blueprint('database', __name__, template_folder='templates')


@database_blueprint.route('/database', methods=['GET', 'POST'])
@login_required
@access_level_required('admin', 'user')
def database():
    return render_template('database/database.html')


@database_blueprint.route('/query', methods=['GET', 'POST'])
@login_required
@access_level_required('admin', 'user')
def query():
    search_string = request.args.get("search_string")

    if search_string:
        results = DbManager.query_products(search_string)
    else:
        db = DbManager()
        results = db.get_all_products()

    return render_template("database/query_results.html", results=results)


@database_blueprint.route('/<int:product_id>/<int:mode>/adjust_stock', methods=['GET', 'POST'])
@login_required
@access_level_required('admin', 'user')
def adjust_stock(product_id, mode):
    db = DbManager()
    try:
        db.adjust_stock(product_id, mode)
    except (ValueError, ProductNotFoundError):
        pass
    search_string = request.args.get("search_string")

    if search_string:
        results = DbManager.query_products(search_string)
    else:

        results = []

    return render_template("database/database.html", results=results)


@database_blueprint.route('/<int:product_id>/<int:current_level>/change_reorder_level', methods=['GET', 'POST'])
@login_required
@access_level_required('admin')
def change_reorder_level(product_id, current_level):

    form = RequiredStockForm()

    if form.validate_on_submit():
        db = DbManager()
        # change stock level with check it can't be below zero
        try:
            db.change_stock_required_level(product_id, form.new_level.data)
        except (ValueError, ProductNotFoundError):
            pass
        return render_template("database/database.html")

    return render_template('database/change_reorder_level.html', form=form, current_level=current_level)


@database_blueprint.route('/add_product', methods=['GET', 'POST'])
@login_required
@access_level_required('admin', 'user')
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        db = DbManager()
        db.add_product(form.name.data,
                       form.stock.data,
                       form.category.data,
                       form.required_stock.data)
        return render_template("database/database.html")

    return render_template('database/add_product.html', form=form)


@database_blueprint.route('/<int:product_id>/delete_product', methods=['GET', 'POST'])
@login_required
@access_level_required('admin')
def delete_product(product_id):
    db = DbManager()
    try:
        db.delete_product(product_id)
    except ProductNotFoundError:
        pass
    search_string = request.args.get("search_string")

    if search_string:
        results = DbManager.query_products(search_string)

    else:
        results = []

    return render_template("database/database.html", results=results)
