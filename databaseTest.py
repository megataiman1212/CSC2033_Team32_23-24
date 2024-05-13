from app import db,app
from models import Product, User

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(User(email="admin@admin.com", password="admin123!", access_level="admin"))
    db.session.add(Product(product="Beans", stock=20, category="food", required_level=30))
    db.session.add(Product(product="Carrots", stock=10, category="food", required_level=0))
    db.session.add(Product(product="Spinach", stock=0, category="food", required_level=5))
