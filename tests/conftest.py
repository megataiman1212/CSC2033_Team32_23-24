from app import app
from models import Product, User
import pytest
from sqlmodel import Session

from Database_Manager.db_crud import DbManager


@pytest.fixture
def stocked_food_product():
    """
    Creates an un stocked product
    :return: a product object
    """

    stocked_food_product = Product(product="Beans", stock=50, category="food", required_level=30)
    yield stocked_food_product


@pytest.fixture
def un_stocked_food_product():
    un_stocked_food_product = Product(product="Grapes", stock=5, category="food", required_level=25)

    yield un_stocked_food_product


@pytest.fixture
def zero_stock_food_product():
    """
    Create a product with 0 stock
    :return: a food product
    """

    zero_stock_food_product = Product(product="Bacon", stock=0, category="food", required_level=20)

    yield zero_stock_food_product


@pytest.fixture
def non_admin_user():

    non_admin_user = User(email= "Test@Test.com", password="password123", access_level="user")

    yield non_admin_user



@pytest.fixture
def db_instance(scope="session"):
    db = DbManager()
    #Create a DB Instance
    yield db


@pytest.fixture(scope="function")
def db_instance_empty(db_instance):

    #Create a fresh database

    db_instance.reset_db()

    yield db_instance

    db_instance.reset_db()




# @pytest.fixture
# def session(db_instance, scope="session"):
#
#     # Create a session,close after test session, uses 'db_instance' fixture
#     with app.app_context():
#         session = Session(db_instance.engine)
#         yield session
#         session.close()



