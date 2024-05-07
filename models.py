#
#
# class User(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True)
#
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     password = db.Column(db.String(100), nullable=False)
#
#     access_level = db.Column(db.String(100), nullable=False)
#
#     def __init__(self,email, password, access_level="user"):
#         self.email = email
#         self.password = password
#         self.access_level = access_level
#
# class Product(db.Model):
#     product_id = db.Column(db.Integer, primary_key=True)
#
#     product = db.Column(db.String(100))
#     stock = db.Column(db.Integer)
#     category = db.Column(db.String(100))
#     required_level = db.Column(db.Integer)
#
#     def __init__(self, product, stock, category, required_level):
#         self.product = product
#         self.stock = stock
#         self.category = category
#         self.required_level = required_level

