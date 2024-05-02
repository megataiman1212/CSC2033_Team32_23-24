from app import db, app

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    accessLevel = db.Column(db.String(100), nullable=False)

    def __init__(self,email, password, accesslevel="user"):
        self.email = email
        self.password = password
        self.accessLevel = accesslevel

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@email.com', password="admin123!",accesslevel="admin")
        db.session.add(admin)
        db.session.commit()


# Run this to initialise db
#init_db()