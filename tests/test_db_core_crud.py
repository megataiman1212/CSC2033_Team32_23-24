from app import app
def add_products(db_instance_empty, stocked_food_product, unstocked_food_product):

    # Adds the two pre-made products to a temporary  in the db
    db_instance_empty.create_product(product=stocked_food_product)
    db_instance_empty.create_product(product=unstocked_food_product)


def test_get_required_stock(db_instance_empty,
                            stocked_food_product, unstocked_food_product):

    add_products(db_instance_empty, stocked_food_product, unstocked_food_product)

    with app.app_context():
        test_stock = db_instance_empty.get_required_stock()

    # Check list is only one item (as only one fits parameter)
    assert len(test_stock) == 1
    assert test_stock[0].product == unstocked_food_product.product


def test_get_all_product(db_instance_empty, stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty, stocked_food_product, unstocked_food_product)

    test_product = db_instance_empty.get_all_products()

    # Checks list is length 2 and has both products
    assert len(test_product) == 2
    assert test_product[0].product == stocked_food_product.product
    assert test_product[1].product == unstocked_food_product.product


# Tests by adding a product and then searching for it
def test_query_products(db_instance_empty, stocked_food_product, unstocked_food_product):

    add_products(db_instance_empty, stocked_food_product, unstocked_food_product)

    with app.app_context():
        # Runs the query_product function and stores result in a list
        test_stocked_food_product = db_instance_empty.query_products(
                                           search_string=stocked_food_product.product)
        test_unstocked_food_product = db_instance_empty.query_products(
                                                                       search_string=unstocked_food_product.product)

    # Checks the found items match the added items (probably only need to check one
    assert test_stocked_food_product[0].stock == stocked_food_product.stock
    assert test_stocked_food_product[0].product == stocked_food_product.product
    assert test_stocked_food_product[0].category == stocked_food_product.category
    assert test_stocked_food_product[0].required_level == stocked_food_product.required_level
    assert test_stocked_food_product[0].product_id == stocked_food_product.product_id
    assert test_unstocked_food_product[0].product == unstocked_food_product.product


def test_adjust_stock(db_instance_empty, stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty, stocked_food_product, unstocked_food_product)

    # get original stock
    pre_unstocked_stock = unstocked_food_product.stock
    pre_stocked_stock = stocked_food_product.stock

    # Increase stock
    db_instance_empty.adjust_stock(product_id=stocked_food_product.product_id, mode=True)
    db_instance_empty.adjust_stock(product_id=unstocked_food_product.product_id, mode=False)

    with app.app_context():
        # searches for stocks
        increase_stock = db_instance_empty.query_products(search_string=stocked_food_product.product)
        decrease_stock = db_instance_empty.query_products(search_string=unstocked_food_product.product)

    # check increased has increased stock by one
    assert increase_stock[0].stock == (pre_stocked_stock + 1)
    assert decrease_stock[0].stock == (pre_unstocked_stock - 1)


def test_change_stock_level(db_instance_empty, stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty,stocked_food_product, unstocked_food_product)

    # Change order level
    db_instance_empty.change_stock_level(product_id=stocked_food_product.product_id, new_stock=100)

    with app.app_context():
        # searches for stocks
        change_stock = db_instance_empty.query_products(search_string=stocked_food_product.product)
        same_stock = db_instance_empty.query_products(search_string=unstocked_food_product.product)

    # Check order level as changed
    assert change_stock[0].stock == 100
    assert same_stock[0].stock == unstocked_food_product.stock


def test_delete_product(db_instance_empty,stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty,stocked_food_product, unstocked_food_product)

    # Get original length
    pre_deletion = len(db_instance_empty.get_all_products())

    # Delete a product
    db_instance_empty.delete_product(product_id=stocked_food_product.product_id)

    # Get all products
    post_deletion = db_instance_empty.get_all_products()

    # Test product has been deleted
    assert len(post_deletion) == (pre_deletion - 1)
    assert post_deletion[0].product == unstocked_food_product.product


def test_get_all_users(db_instance_empty,non_admin_user):
    db_instance_empty.create_user(user=non_admin_user)

    # Get all users
    all_users = db_instance_empty.get_all_users()

    # Test all users are gathered
    assert len(all_users) == 2


#
# def test_change_password(db_instance_empty, , non_admin_user):
#     db_instance_empty.create_user(user=non_admin_user, =)
#
#     db_instance_empty.change_password(=, user_id=non_admin_user.user_id, current_password=non_admin_user.password, new_password="Change123")
#
#     updated_user =

def test_get_user(db_instance_empty, non_admin_user):
    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    #Check user has been retrieved
    user = db_instance_empty.get_user("Test@Test.com")
    assert user == non_admin_user

def test_add_staff(db_instance_empty):
    # Add non admin user
    db_instance_empty.add_staff("Test@Test.com", "password123", "user")

    #Get user
    user = db_instance_empty.get_user("Test@Test.com")
    # Check user details match
    assert user.email == "Test@Test.com"
    assert user.password == "password123"
    assert user.access_level == "user"

def test_add_product(db_instance_empty):
    #Add stock
    with app.app_context():
        db_instance_empty.add_product("Beans", 50, "food", 30)
        #get stock
        stock = db_instance_empty.query_products("Beans")
    assert stock[0].stock == 50
    assert stock[0].product == "Beans"
    assert stock[0].category == "food"
    assert stock[0].required_level == 30

def test_delete_staff(db_instance_empty,non_admin_user):
    #Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    #Test delete
    db_instance_empty.delete_staff("Test@Test.com")
    users = db_instance_empty.get_all_users()
    assert len(users) == 1

def test_verify_password(db_instance_empty,non_admin_user):

    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    assert db_instance_empty.verify_password("Test@Test.com", "password123")

def test_find_user(db_instance_empty, non_admin_user):
    db_instance_empty.create_user(user=non_admin_user)

