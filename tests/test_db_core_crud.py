import pytest
from Database_Manager.db_crud import UserNotFoundError
from app import app
from pytest import raises

def add_products(db_instance_empty, stocked_food_product, un_stocked_food_product):
    """
    Adds the two pre-made products to a temporary  in the db
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: is a food product which is un stocked (stock < required level)
    """
    
    db_instance_empty.create_product(product=stocked_food_product)
    db_instance_empty.create_product(product=un_stocked_food_product)


def test_get_required_stock(db_instance_empty,
                            stocked_food_product, un_stocked_food_product):
    """
    tests the get_required_stock function
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: food product which is un stocked (stock < required level)
    """
    add_products(db_instance_empty, stocked_food_product, un_stocked_food_product)

    #  this gets all the un stocked products
    with app.app_context():
        test_stock = db_instance_empty.get_required_stock()

    # check list is only one item (as only one fits parameter)
    assert len(test_stock) == 1

    # checks the product found matches the un stocked product
    assert test_stock[0].product == un_stocked_food_product.product


def test_get_all_product(db_instance_empty, stocked_food_product, un_stocked_food_product):
    """
    tests the get_all_product function
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: food product which is un stocked (stock < required level)
    """
    add_products(db_instance_empty, stocked_food_product, un_stocked_food_product)

    test_product = db_instance_empty.get_all_products()

    # Checks list is length 2 and has both products
    assert len(test_product) == 2
    assert test_product[0].product == stocked_food_product.product
    assert test_product[1].product == un_stocked_food_product.product


def test_query_products(db_instance_empty, stocked_food_product, un_stocked_food_product):
    """
    tests the query_products function by adding items and then searching for them
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: food product which is un stocked (stock < required level)
    """
    add_products(db_instance_empty, stocked_food_product, un_stocked_food_product)

    with app.app_context():
        # Runs the query_product function and stores result in a list
        test_stocked_food_product = db_instance_empty.query_products(
                                           search_string=stocked_food_product.product)
        test_un_stocked_food_product = db_instance_empty.query_products(
                                                                       search_string=un_stocked_food_product.product)

    # Checks the found items match the added items (probably only need to check one but did all to be sure)
    assert test_stocked_food_product[0].stock == stocked_food_product.stock
    assert test_stocked_food_product[0].product == stocked_food_product.product
    assert test_stocked_food_product[0].category == stocked_food_product.category
    assert test_stocked_food_product[0].required_level == stocked_food_product.required_level
    assert test_stocked_food_product[0].product_id == stocked_food_product.product_id
    assert test_un_stocked_food_product[0].product == un_stocked_food_product.product


def test_query_products_not_string(db_instance_empty):
    """
    test query_products when None is passed
    :param db_instance_empty: cretaes an empty database
    """
    with app.app_context():
        # Ensure that a TypeError is raised when search_string is None
        with pytest.raises(TypeError):
            db_instance_empty.query_products(search_string=None)


def test_adjust_stock(db_instance_empty, stocked_food_product, un_stocked_food_product):
    """
    tests the adjust_stock function by getting original stock, changing it and then re checking stock
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: food product which is un stocked (stock < required level)
    """
    add_products(db_instance_empty, stocked_food_product, un_stocked_food_product)
    # Get original stock
    pre_un_stocked_stock = un_stocked_food_product.stock
    pre_stocked_stock = stocked_food_product.stock

    # Increase stock
    db_instance_empty.adjust_stock(product_id=stocked_food_product.product_id, mode=True)
    db_instance_empty.adjust_stock(product_id=un_stocked_food_product.product_id, mode=False)

    with app.app_context():
        # searches for stocks
        increase_stock = db_instance_empty.query_products(search_string=stocked_food_product.product)
        decrease_stock = db_instance_empty.query_products(search_string=un_stocked_food_product.product)

    # checks stock levels have changed
    assert increase_stock[0].stock == (pre_stocked_stock + 1)
    assert decrease_stock[0].stock == (pre_un_stocked_stock - 1)


def test_adjust_stock_not_bool(db_instance_empty, stocked_food_product, un_stocked_food_product):
    """
    test adjust stock when mode isn't a bool
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: food product which is un_stocked (stock < required level)
    """
    add_products(db_instance_empty, stocked_food_product, un_stocked_food_product)

    # Increase stock
    with pytest.raises(TypeError):
        db_instance_empty.adjust_stock(product_id=stocked_food_product.product_id, mode=None)
        db_instance_empty.adjust_stock(product_id=un_stocked_food_product.product_id, mode="Fail")


def test_adjust_stock_below_zero(db_instance_empty, zero_stock_food_product):
    """
    Tests if you can move stock below zero
    :param db_instance_empty: creates an empty database
    :param zero_stock_food_product: a product object with 0 stock
    """

    db_instance_empty.create_product(product=zero_stock_food_product)

    with pytest.raises(ValueError):
        db_instance_empty.adjust_stock(product_id=zero_stock_food_product.product_id, mode=False)


def test_change_stock_level(db_instance_empty, stocked_food_product, un_stocked_food_product):
    """
    tests change_stock_level function
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: food product which is un stocked (stock < required level)
    """
    add_products(db_instance_empty, stocked_food_product, un_stocked_food_product)

    # Change order level
    db_instance_empty.change_stock_level(product_id=stocked_food_product.product_id, new_stock=100)

    with app.app_context():
        # searches for stocks
        change_stock = db_instance_empty.query_products(search_string=stocked_food_product.product)
        same_stock = db_instance_empty.query_products(search_string=un_stocked_food_product.product)

    # Check order level as changed
    assert change_stock[0].stock == 100
    assert same_stock[0].stock == un_stocked_food_product.stock


def test_delete_product(db_instance_empty, stocked_food_product, un_stocked_food_product):
    """
    test delete_product function
    :param db_instance_empty: creates an empty database
    :param stocked_food_product: food product which is stocked (stock > required level)
    :param un_stocked_food_product: food product which is un stocked (stock < required level)
    """
    add_products(db_instance_empty, stocked_food_product, un_stocked_food_product)

    # Get original length
    pre_deletion = len(db_instance_empty.get_all_products())

    # Delete a product
    db_instance_empty.delete_product(product_id=stocked_food_product.product_id)

    # Get all products
    post_deletion = db_instance_empty.get_all_products()

    # Test product has been deleted
    assert len(post_deletion) == (pre_deletion - 1)
    assert post_deletion[0].product == un_stocked_food_product.product


def test_get_all_users(db_instance_empty, non_admin_user):
    """
    test get_all_users function
    :param db_instance_empty: creates an empty database
    :param non_admin_user: a user without admin privilege
    """
    db_instance_empty.create_user(user=non_admin_user)

    # Get all users
    all_users = db_instance_empty.get_all_users()

    # Test all users are gathered
    assert len(all_users) == 2


def test_change_password(db_instance_empty, non_admin_user):
    """
    test change_password function
    :param db_instance_empty: creates an empty database
    :param non_admin_user: a user without admin privilege
    """

    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    #Check fails if wrong password
    assert db_instance_empty.change_password(user_id=non_admin_user.user_id, current_password="wrong",
                                             new_password="Change123") == "wrong password"
    assert db_instance_empty.change_password(user_id=non_admin_user.user_id, current_password="password123",
                                             new_password="password123") == "same password"
    # Update password
    db_instance_empty.change_password(user_id=non_admin_user.user_id, current_password="password123",
                                      new_password="Change123")
    # Check password updated
    assert db_instance_empty.verify_password(non_admin_user.email, "Change123")


def test_get_user(db_instance_empty, non_admin_user):
    """
        test get_user function
        :param db_instance_empty: creates an empty database
        :param non_admin_user: a user without admin privilege
        """
    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    # Check user has been retrieved
    user = db_instance_empty.get_user("Test@Test.com")
    assert user == non_admin_user

def test_get_user_wrong_data(db_instance_empty, non_admin_user):
    """
            test get_user function
            :param db_instance_empty: creates an empty database
            :param non_admin_user: a user without admin privilege
            """
    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    with pytest.raises(ValueError):
        user = db_instance_empty.get_user(0)


def test_add_staff(db_instance_empty):
    """
    test add_staff function
    :param db_instance_empty: creates an empty database
    """
    # Add non admin user
    db_instance_empty.add_staff("Test@Test.com", "password123", "user")

    # Get user
    user = db_instance_empty.get_user("Test@Test.com")
    # Check user details match
    assert user.email == "TEST@TEST.COM"
    assert db_instance_empty.verify_password(email="Test@Test.com", test_password="password123")
    assert user.access_level == "user"

def test_add_staff_wrong_data(db_instance_empty):
    """
    test adding staff with wrong data types
    """
    with pytest.raises(TypeError):
        db_instance_empty.add_staff(10, "password123", "user")
    with pytest.raises(TypeError):
        db_instance_empty.add_staff("Test@Test.com", 10, "user")
    with pytest.raises(ValueError):
        db_instance_empty.add_staff("Test@Test.com", "password123", "wrong")


def test_add_product(db_instance_empty):
    """
    test add_product function
    :param db_instance_empty: creates an empty database
    """
    # Add stock
    with app.app_context():
        db_instance_empty.add_product("Beans", 50, "food", 30)
        # get stock
        stock = db_instance_empty.query_products("Beans")
    assert stock[0].stock == 50
    assert stock[0].product == "Beans"
    assert stock[0].category == "food"
    assert stock[0].required_level == 30

    # Test if product already exists
    with app.app_context():
        db_instance_empty.add_product("Beans", 50, "food", 30)
        # get stock
        stock = db_instance_empty.query_products("Beans")
    # check duplicate no added
    assert len(db_instance_empty.get_all_products()) == 1
    # Check stock has been appended since duplicate added
    assert stock[0].stock == 100

def test_add_product_wrong_data(db_instance_empty):
    """
    test add_product function with wrong data types for the product
    """
    with pytest.raises(TypeError):
        with app.app_context():
            db_instance_empty.add_product(10, 50, "food", 30)
    with pytest.raises(TypeError):
        with app.app_context():
            db_instance_empty.add_product("Beans", "50", "food", 30)
    with pytest.raises(ValueError):
        with app.app_context():
            db_instance_empty.add_product("beans", 50, "wrong", 30)
    with pytest.raises(TypeError):
        with app.app_context():
            db_instance_empty.add_product("beans", 50, "food", "30")


def test_delete_staff(db_instance_empty, non_admin_user):
    """
    test delete_staff function
    :param db_instance_empty: creates an empty database
    :param non_admin_user: a user without admin privilege
    """
    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    # Test delete non existing user
    with pytest.raises(UserNotFoundError):
        db_instance_empty.delete_staff("wrong_email")
    # Test delete user
    db_instance_empty.delete_staff("Test@Test.com")
    # Test error thrown as staff deleted
    with pytest.raises(UserNotFoundError):
        db_instance_empty.get_user("Test@Test.com")


def test_verify_password(db_instance_empty, non_admin_user):
    """
    test verify_password function
    :param db_instance_empty: creates an empty database
    :param non_admin_user: a user without admin privilege
    """
    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    assert db_instance_empty.verify_password("Test@Test.com", "password123")
    # Check method returns false with wrong password
    assert db_instance_empty.verify_password("Test@Test.com", "wrong password") is False


def test_verify_password_wrong_data(db_instance_empty, non_admin_user):
    """
    test verify_password function
    :param db_instance_empty: creates an empty database
    :param non_admin_user: a user without admin privilege
    """
    # Add non admin user
    db_instance_empty.create_user(user=non_admin_user)
    # Check error is thrown if user doesn't exist
    with pytest.raises(UserNotFoundError):
        db_instance_empty.verify_password("wrong_email", "password")
