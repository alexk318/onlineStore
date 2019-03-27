from webAppFile import db  # SQLAlchemy class instance

# UserMixin automatically defines 'is_authenticated', 'is_active', 'is_anonymous', and 'get_id' methods
from flask_security import UserMixin, RoleMixin

from datetime import datetime

from re import sub  # The function is responsible for changing the bad characters to some one

role_user_link = db.Table('role_user',
                          db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                          db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                          )  # Each user id is associated with a privilege id


class User(db.Model, UserMixin):  # User - Model ; User - Table in 'onlinestoredb' database
    # primary_key - Unique identification of table entries
    id = db.Column(db.Integer(), primary_key=True)  # Column in the database with the data type Integer
    name = db.Column(db.String(50))  # Real person's name
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)  # E-mail must be unique
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    # Linking 'User' and 'Role'
    # 'Role' - Related model. 'role_user_link' - Table with data for linking relationships.
    # 'relatedusers' - Property for class 'Role'. 'dynamic' - When appealing, we get a BaseQuery object
    # 'roles' is a MANDATORY property for 'user_datastore'!
    roles = db.relationship('Role', secondary=role_user_link, backref=db.backref('related_users', lazy='dynamic'))

    def __repr__(self):  # repr - Represents the output of the class object in a more readable form.
        return '<User ID: {}, Email: {}>'.format(self.id, self.email)  # format to substitute values in braces

    # There are three roles:
    # Administrator [Has access to the admin panel and can add all to the blacklist.]
    # Moderator [Verifies user posts. Only regular users can add to the blacklist.]
    # Regular user [Everyone who registers automatically receives this role.]


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)  # 'name' is a MANDATORY property for 'Role'!

    def __repr__(self):
        return '<Role ID: {}, Title: {}>'.format(self.id, self.name)


def slugify(string):
    # The template accepts all characters except those that are not allowed for URLs
    # [pythex.org]
    pattern = r'[^\w+]'

    # Return a string by pattern, replacing unwanted characters on the dash
    return sub(pattern, '-', str(string))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text)
    img_title = db.Column(db.String(255))
    headline = db.Column(db.String(35))  # With 36 characters, the headline starts to go beyond the item card
    description = db.Column(db.String(50))
    text = db.Column(db.Text)
    cost = db.Column(db.String(5))
    slug = db.Column(db.String(255), unique=True)  # Human-readable URL
    date_creation = db.Column(db.String(10), default=datetime.today().strftime("%d.%m.%Y"))

    def slug_generate(self):
        if self.headline:
            self.slug = slugify(self.headline)

    def __init__(self, *args, **kwargs):  # Making settings before class
        super(Product, self).__init__(*args, **kwargs)  # Call db.Model
        self.slug_generate()

    def __repr__(self):
        return '<Product id: {}, headline: {}>'.format(self.id, self.headline)



