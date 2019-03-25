from flask import Blueprint, render_template, request

from configurationFile import database_cursor, connection_link

# A decorator that allows only authorized users to log in to a specific View
from flask_security import login_required, current_user

from modelsFile import Product

from webAppFile import db

# Shopping has a branch of addresses in it, so Blueprint is used here
# Blueprint name, __name__, Folder with HTML
blueprint_instance = Blueprint('buypage', __name__, template_folder='templates')


@blueprint_instance.route('/')
@login_required
def products_page():
    """Page Handler '/buy'"""

    products_list = Product.query.all()

    return render_template('products_page.html', products_list=products_list)


@blueprint_instance.route('/<slug>')
@login_required
def product_link(slug):
    """Handler full product page"""
    # First() is specified, because the return type of filter is BaseQuery.
    # BaseQuery does not have the necessary functionality. first() removes the BaseQuery type.
    specific_product = Product.query.filter(Product.slug == slug).first()

    #cart = list()

    #if request.method == 'POST':

       # cart.append(specific_product.id)

        #session["cart"] = cart

        #return render_template('welcome.html')

    return render_template('link.html', specific_product=specific_product)


@blueprint_instance.route('/<slug>/addToCart', methods=['GET'])
@login_required
def add_to_cart(slug):

    if request.method == 'GET':

        specific_product = Product.query.filter(Product.slug == slug).first()

        product_id = specific_product.id

        user_id = current_user.id

        database_cursor.execute("INSERT INTO Cart (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
        connection_link.commit()

        return render_template('welcome.html', specific_product=specific_product)


