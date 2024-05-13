from app import app
from models import Product
import pytest
from sqlmodel import Session

from Database_Manager.db_CRUD import DB_Manager

# create a product that is in stock
@pytest.fixture
def stocked_food_product():

    # Creates a product to test in the database
    stocked_food_product = Product(product="Beans", stock=50, category="food", required_level=30)
    yield stocked_food_product

#create a product that is not in stock
@pytest.fixture
def unstocked_food_product():

    unstocked_food_product = Product(product="Grapes", stock=5, category="food", required_level=25)

    yield unstocked_food_product

@pytest.fixture
def db_instance(scope="session"):
    db = DB_Manager()
    #Create a DB Instance
    yield db


@pytest.fixture
def session(db_instance, scope="session"):

    # Create a session,close after test session, uses 'db_instance' fixture
    with app.app_context():
        session = Session(db_instance.engine)
        yield session
        session.close()


@pytest.fixture(scope="function")
def db_instance_empty(db_instance, session):

    # Create a fresh database

    db_instance.delete_all_products(session)

    yield db_instance

    db_instance.delete_all_products(session)



