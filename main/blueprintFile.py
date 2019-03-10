from flask import Blueprint, render_template  # Shopping has a branch of addresses in it, so Blueprint is used here

from flask_security import login_required  # A decorator that allows only authorized users to log in to a specific View

from modelsFile import Product

# Blueprint name, __name__, Folder with HTML
blueprint_instance = Blueprint('buypage', __name__, template_folder='templates')


@blueprint_instance.route('/')
@login_required
def products_page():
    products_list = Product.query.all()
    return render_template('products_page.html', products_list=products_list)


@blueprint_instance.route('/<slug>')
@login_required
def product_link(slug) -> object:
    # First() is specified, because the return type of filter is BaseQuery.
    # BaseQuery does not have the necessary functionality. first() removes the BaseQuery type.
    specific_product = Product.query.filter(Product.slug == slug).first()
    return render_template('link.html', specific_product=specific_product)

