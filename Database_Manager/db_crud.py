"""This Module contains all the crud methods"""
from sqlmodel import Session
from sqlalchemy import create_engine
from models import Product, User
from app import app
class DbManager():
    """Class containing all the crud methods which interact with the database"""
    def __init__(self):
        # Define the database URI
        db_uri = 'mysql+pymysql://root:Team32@localhost/Inventory'

        # Create the engine (used for CRUD)
        engine = create_engine(db_uri, echo=True)
        self.engine = engine
        self.session = Session(engine)
    
    def __del__(self):
        # Close the self.session when the class is destroyed
        self.session.close()

    def create_product(self, product: Product) -> None:
        """
        Create a product in the database (used for testing)

        :param product: The product to create
        """
        # Write to database
        self.session.add(product)
        self.session.commit()

    def create_user(self, user):
        """
        create user (used for testing)
        :param user: user to be added
        """
        self.session.add(user)
        self.session.commit()
    
    def reset_db(self):
        """
        Delete all products in the database
        """
        try:
            self.session.query(Product).delete()
            self.session.query(User).delete()
            self.session.add((User(email="admin@admin.com", password="admin123!", access_level="admin")))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

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
    def get_all_products(self):
        """
        Get all products in the database
        :return: A list of product objects
        """
        stock = self.session.query(Product).all()
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
    def add_product(self, product, stock, category, required_level):
        """
        Add a product in the database
        :param product: string product name
        :param stock: int stock of product
        :param category: string either "food" or "hygiene"
        :param required_level: int required level of stock of product
        :return:
        """
        self.session.add(Product(product, stock, category, required_level))
        self.session.commit()

    #FR10
    def adjust_stock(self, product_id, mode):
        """
        Adjust the stock of a product
        :param product_id: int id of the product to adjust
        :param mode: boolean, true to increase by one false to decrease by one
        """
        product_to_edit = self.session.query(Product).get(product_id)
        if mode:
            product_to_edit.stock += 1
        else:
            product_to_edit.stock -= 1

        self.session.commit()

    #FR17
    def change_stock_level(self, product_id, new_stock):
        """
        Change the stock level of a product
        :param product_id: int id of the product to change
        :param new_stock: new stock level of the product
        """
        product = self.session.query(Product).get(product_id)
        product.stock = new_stock
        self.session.commit()

    #FR5
    def delete_product(self, product_id):
        """
        Delete a product from the database
        :param product_id: id of the product to delete
        """
        self.session.delete(self.session.query(Product).get(product_id))
        self.session.commit()

    #FR4
    def get_all_users(self):
        """
        Get all users in the database
        :return: list of user objects
        """
        return self.session.query(User).all()

    #FR2,7
    def change_password(self, user_id, current_password, new_password):
        """
        Change the password of a user
        :param user_id: int id of the user to change password
        :param current_password: string of the current password
        :param new_password: string of the new password
        """
        user = self.session.query(User).get(user_id)
        if user.password == current_password:
            user.password = new_password
            self.session.commit()
        else:
            raise ValueError("Password does not match")

    #FR1,3#
    def add_staff(self, email, password, access_level):
        """
        Add a staff member to the database
        :param email: str email of the staff member
        :param password: str password of the staff member
        :param access_level: str access level of the staff member either "user" or "admin"
        """
        if access_level != ("user" or "admin"):
            raise ValueError("Access level must be user or admin")
        self.session.add(User(email, password, access_level))
        self.session.commit()

    #FR4
    def delete_staff(self, email):
        """
        Delete a staff member from the database
        :param email: int id of the staff member to delete
        """
        self.session.delete(self.session.query(User).filter_by(email=email).first())
        self.session.commit()

    #FR12
    
    def verify_password(self, email, test_password):
        """
        Verify the password of a user
        :param email: email of the user of password to verify
        :param test_password: password to be verified against the users password
        :return: boolean true if password matches false if not
        """
        user = self.session.query(User).filter_by(email=email).first()
        return user.password == test_password

    def get_user(self, email):
        """
        returns a user by searching with their email
        :param email: string email of user to get
        :return: User object
        """
        user = self.session.query(User).filter_by(email=email).first()
        return user
