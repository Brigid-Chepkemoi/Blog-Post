from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager
from datetime import datetime
from . import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    author=db.Column(db.String(255))
    email=db.Column(db.String(255), unique=True, index=True)
    password_hash=db.Column(db.String(255))
    bio=db.Column(db.String(255))
    profile_pic_path=db.Column(db.String())
    blog=db.relationship('Blogs', backref='author', lazy='dynamic')
    comments=db.relationship('Comments', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Author: {self.author}'

    def __int__(self, mail, author, password):
        self.mail=mail
        self.author=author
        self.password=password


class Blogs(db.Model):
    __tablename__='blogs'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(255))
    category=db.Column(db.String(255))
    blog=db.Column(db.String(255))
    date=db.Column(db.DateTime(250), default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    comments=db.relationship('Comments', backref='title', lazy='dynamic')

    def save_blogs(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls, cate):
        """

        :rtype: object
        """
        blogs=Blogs.query.filter_by(category=cate).all()
        return blogs

    def __repr__(self):
        return f"Blogs {self.blogs}','{self.date}')"


class Comments(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer, primary_key=True)
    comment=db.Column(db.String(255))
    date_posted=db.Column(db.DateTime(250), default=datetime.utcnow)
    blogs_id=db.Column(db.Integer, db.ForeignKey("blogs.id"))
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comment(cls, id):
        comments=Comments.query.filter_by(blogs_id=id).all()
        return comments

    def __repr__(self):
        return f"Comments('{self.comment}', '{self.date_posted}')"


class Quote:
    def __init__(self, author, quote):
        self.author=author
        self.quote=quote
