"""This Module contains all the crud methods"""
from sqlmodel import Session
from sqlalchemy import create_engine
from models import Product, User
import bcrypt
from app import app

class UserNotFoundError(Exception):
    pass
class DbManager:
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
            self.session.add((User(email="admin@admin.com", password="Admin123!", access_level="admin")))
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

    # FR8
    def get_all_products(self):
        """
        Get all products in the database
        :return: A list of product objects
        """
        with app.app_context():
            stock = self.session.query(Product).all()
            print(stock)
            return stock

    # FR15
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

    # FR9
    def add_product(self, product, stock, category, required_level):
        """
        Add a product in the database if already exist then add stock to product
        :param product: string product name
        :param stock: int stock of product
        :param category: string either "food" or "hygiene"
        :param required_level: int required level of stock of product
        :return:
        """
        dupe_product = self.session.query(Product).filter_by(product=product).first()
        if dupe_product:
            self.change_stock_level(dupe_product.product_id, dupe_product.stock + stock)
        else:
            self.session.add(Product(product, stock, category, required_level))
        self.session.commit()

    # FR10
    def adjust_stock(self, product_id, mode):
        """
        Adjust the stock of a product
        :param product_id: int id of the product to adjust
        :param mode: boolean, true to increase by one false to decrease by one
        """
        if not isinstance(mode, int):
            raise TypeError("Mode must be a int")
        product_to_edit = self.session.query(Product).get(product_id)
        if mode:
            product_to_edit.stock += 1
        else:
            if product_to_edit.stock > 0:
                product_to_edit.stock -= 1
            else:
                raise ValueError("Stock can't go below zero")
        self.session.commit()

    # FR17
    def change_stock_level(self, product_id, new_level):
        """
        Change the stock level of a product
        :param product_id: int id of the product to change
        :param new_level: new required level of the product
        """
        product = self.session.query(Product).get(product_id)
        product.stock = new_level
        self.session.commit()

    def change_stock_required_level(self, product_id, new_level):
        """
        Change the required stock level of a product
        :param product_id: int id of the product to change
        :param new_level: new required level of the product
        """
        product = self.session.query(Product).get(product_id)
        product.required_level = new_level
        self.session.commit()

    # FR5
    def delete_product(self, product_id):
        """
        Delete a product from the database
        :param product_id: id of the product to delete
        """
        self.session.delete(self.session.query(Product).get(product_id))
        self.session.commit()

    # FR4
    def get_all_users(self):
        """
        Get all users in the database
        :return: list of user objects
        """
        return self.session.query(User).all()

    # FR2,7
    def change_password(self, user_id, current_password, new_password):
        """
        Change the password of a user
        :param user_id: int id of the user to change password
        :param current_password: string of the current password
        :param new_password: string of the new password
        """
        if not isinstance(user_id,int):
            raise TypeError("User id must be int")
        if not isinstance(current_password,str):
            raise TypeError("Current_password must be string")
        if not isinstance(new_password,str):
            raise TypeError("New_password must be string")
        user = self.session.query(User).get(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            encoded_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            if bcrypt.checkpw(new_password.encode('utf-8'), user.password.encode('utf-8')):
                # if user tries to change password to same password
                return "same password"
            else:
                user.password = encoded_new_password
                self.session.commit()
        else:
            # if user enters current password wrong
            return "wrong password"

    # FR1,3
    def add_staff(self, email, password, access_level):
        """
        Add a staff member to the database
        :param email: str email of the staff member
        :param password: str password of the staff member
        :param access_level: str access level of the staff member either "user" or "admin"
        """
        if access_level == "user" or access_level == "admin":
            self.session.add(User(email, password, access_level))
            self.session.commit()
        else:
            raise ValueError("access_level must be either user or admin")

    # FR4
    def delete_staff(self, email):
        """
        Delete a staff member from the database
        :param email: int id of the staff member to delete
        """
        user = self.get_user(email)
        self.session.delete(user)
        self.session.commit()

    # FR12
    
    def verify_password(self, email, test_password):
        """
        Verify the password of a user
        :param email: email of the user of password to verify
        :param test_password: password to be verified against the users password
        :return: boolean true if password matches false if not
        """
        user = self.get_user(email)
        if not user:
            raise ("User does not exist")

        # Ensure the stored hashed password is in bytes
        stored_hashed_password = user.password.encode('utf-8')

        return bcrypt.checkpw(test_password.encode('utf-8'), stored_hashed_password)

    def get_user(self, email):
        """
        returns a user by searching with their email
        :param email: string email of user to get
        :return: User object
        """
        #Check email is string
        if not isinstance(email,str):
            raise ValueError("Email must be a string")
        email = email.upper()  # Upper email as all emails stored in upper case
        # get user and check they exist
        user = self.session.query(User).filter_by(email=email).first()
        if not user:
            raise UserNotFoundError("User does not exist")
        return user
