from shop import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=128), nullable=False, unique=True)
    email = db.Column(db.String(length=128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    items = db.relationship('Item', backref='owner_user')

    def __repr__(self):
        return f'{self.username} {self.email} {self.password_hash}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.password_hash.encode('utf-8'), plain_password)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    price = db.Column(db.Float(), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.title} {self.description} {self.price} {self.owner}'