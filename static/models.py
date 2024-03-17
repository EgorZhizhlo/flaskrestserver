from flask import Flask
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class POSTS(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    datetime = db.Column(db.String(120), unique=False, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    text = db.Column(db.String(1000), unique=False, nullable=False)


class USERS(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(1000), unique=False, nullable=False)
    repeat_password = db.Column(db.String(1000), unique=False, nullable=False)
    admin = db.Column(db.Integer, unique=False, nullable=False, default=0)


with app.app_context():
    db.create_all()
    admins = USERS.query.filter_by(username='yooo-boy').first()
    if admins is None:
        db.session.add(
            USERS(username='yooo-boy', email='ezhizhlo@mail.ru',
                  password=generate_password_hash('CgFuhy@g9XBc'),
                  repeat_password=generate_password_hash('CgFuhy@g9XBc'),
                  admin=1
                  )
        )
        db.session.commit()
