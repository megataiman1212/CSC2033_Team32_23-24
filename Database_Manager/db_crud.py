"""This Module contains all the crud methods"""
from sqlmodel import Session
from sqlalchemy import create_engine
from models import Product, User
class DbManager():
    """Class containing all the crud methods which interact with the database"""
    def __init__(self):
        # Define the database URI
        db_uri = 'mysql+pymysql://root:Team32@localhost/Inventory'

        # Create the engine (used for CRUD)
        engine = create_engine(db_uri, echo=True)
        self.engine = engine

    @staticmethod
    def create_product(product: Product, session: Session) -> None:
        """
        Create a product in the database

        :param product: The product to create
        :param session: The database session
        """
        # Write to database
        session.add(product)
        session.commit()

    @staticmethod
    def create_user(user, session):

        session.add(user)
        session.commit()

    @staticmethod
    def delete_all_products(session):
        """
        Delete all products in the database

        :param session: The database session
        """
        try:
            session.query(Product).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # FR11
    @staticmethod
    def get_required_stock():
        """
        Get a list of products with stock below the required stock
        :return: A list of Product objects
        """
        stock = Product.query.filter(Product.stock < Product.required_level).all()
        return stock

    #FR8
    @staticmethod
    def get_all_products(session):
        """
        Get all products in the database
        :return: A list of product objects
        """
        stock = session.query(Product).all()
        return stock

    #FR15
    @staticmethod
    def query_products(search_string):
        """
        Returns any products that contain the substring search_string
        :param search_string: String to search (not case dependant)
        :return: list of product objects
        """
        if not isinstance(search_string, str):
            raise TypeError("SearchString must be a string")
        stock = Product.query.all()
        searched_stock = []
        for i in stock:
            if search_string.upper() in i.product.upper():
                searched_stock.append(i)
        return searched_stock

    #FR9
    @staticmethod
    def add_product(session, product, stock, category, required_level):
        """
        Add a prodcut in the database
        :param session: current session
        :param product: string product name
        :param stock: int stock of product
        :param category: string either "food" or "hygiene"
        :param required_level: int required level of stock of product
        :return:
        """
        session.add(Product(product, stock, category, required_level))
        session.commit()

    #FR10
    @staticmethod
    def adjust_stock(session, product_id, mode):
        """
        Adjust the stock of a product
        :param session: current session
        :param product_id: int id of the product to adjust
        :param mode: boolean, true to increase by one false to decrease by one
        """
        product_to_edit = Product.query.get(product_id)
        if mode:
            product_to_edit.stock += 1
        else:
            product_to_edit.stock -= 1
        session.commit()

    #FR17
    @staticmethod
    def change_stock_level(session, product_id, new_stock):
        """
        Change the stock level of a product
        :param session: current session
        :param product_id: int id of the product to change
        :param new_stock: new stock level of the product
        """
        product = session.query(Product).get(product_id)
        product.stock = new_stock
        session.commit()

    #FR5
    @staticmethod
    def delete_product(session, product_id):
        """
        Delete a product from the database
        :param session: current session
        :param product_id: id of the product to delete
        """
        session.delete(session.query(Product).get(product_id))
        session.commit()

    #FR4
    @staticmethod
    def get_all_users(session):
        """
        Get all users in the database
        :return: list of user objects
        """
        return session.query(User).all()

    #FR2,7
    @staticmethod
    def change_password(session, user_id, current_password, new_password):
        """
        Change the password of a user
        :param session: current session
        :param user_id: int id of the user to change password
        :param current_password: string of the current password
        :param new_password: string of the new password
        """
        user = session.query(User).get(user_id)
        if user.password == current_password:
            user.password = new_password
            session.commit()
        else:
            raise ValueError("Password does not match")

    #FR1,3#
    @staticmethod
    def add_staff(session, email, password, access_level):
        """
        Add a staff member to the database
        :param session: current session
        :param email: str email of the staff member
        :param password: str password of the staff member
        :param access_level: str access level of the staff member either "user" or "admin"
        """
        if access_level != ("user" or "admin"):
            raise ValueError("Access level must be user or admin")
        session.add(User(email, password, access_level))
        session.commit()

    #FR4
    @staticmethod
    def delete_staff(session, user_id):
        """
        Delete a staff member from the database
        :param session: current session
        :param user_id: int id of the staff member to delete
        """
        session.delete(session.query(User).get(user_id))
        session.commit()

    #FR12
    @staticmethod
    def verify_password(session, user_id, test_password):
        """
        Verify the password of a user
        :param session: current session
        :param user_id: id of the user of password to verify
        :param test_password: password to be verified against the users password
        :return: boolean true if password matches false if not
        """
        user = session.query(User).get(user_id)
        return user.password == test_password
