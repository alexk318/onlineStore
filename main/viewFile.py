# Flask and Django use pattern MVC:
# Model - Model Description (db)
# View - Data mapping to user
# Controller - Binds user and database, app

from flask import render_template, session  # 'render_template' displays HTML to the page
from flask import request, redirect, url_for
from flask_security import login_required, current_user
from formsFile import RegisterForms, ProductsAddingForms
from webAppFile import app, db, user_datastore
from modelsFile import Product, User
from configurationFile import database_cursor, connection_link
import os


def write_file(data, filename):
    """Writing binary data to file"""
    with open(filename, 'wb') as f:
        f.write(data)


def make_dir_image(fileimage, foldername):
    img_title = fileimage.filename
    dirstr = "static/" + foldername
    os.mkdir(dirstr)  # Creating a folder
    write_file(fileimage.read(), dirstr + "/" + img_title)  # Write a photo to its associated folder


@app.route('/')  # The user can appeal the web application on the path '/'  {'/' : 'welcome_page'}
def welcome_page():  # Define the 'View'
    # The use of tags is adequately perceived, but better to use HTML templates

    return render_template('welcome.html')


@app.route('/profile')
def define_profile():

    return render_template('profile_page.html')

@app.route('/registration', methods=['POST', 'GET'])
def registration_page():

    # Web server accepts data
    if request.method == 'POST':
        # We request forms from the RegisterForm class by writing them into separate variables.
        nameuser = request.form['nameform']
        surnameuser = request.form['surnameform']
        emailuser = request.form['emailform']
        passworduser = request.form['passwordform']
        print(passworduser)

        # Create a user, equating the arguments of the class User to the values entered by the user.
        new_user = user_datastore.create_user(name=nameuser, surname=surnameuser, email=emailuser,
                                              password=passworduser)

        # Adding values to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('welcome_page'))

    # regforms stores all RegisterForm class arguments
    regforms = RegisterForms()

    return render_template('registration.html', regforms=regforms)  # We make a request [GET] to the address


@app.route('/sell', methods=['POST', 'GET'])
@login_required
def add_page():
    adding_products_forms = ProductsAddingForms()
    if request.method == 'POST':

        customheadline = request.form['headlineform']
        if len(customheadline) > 35:
            error = 'The headline must not exceed 35 characters!'
            return render_template('products_add.html', adding_products_forms=adding_products_forms, error=error)

        customtext = request.form['textform']

        customdescription = request.form['descriptionform']
        if len(customdescription) > 50:
            error = 'The description must not exceed 50 characters!'
            return render_template('products_add.html', adding_products_forms=adding_products_forms, error=error)

        customcost = request.form['costform']
        if not customcost.isdigit():
            error = 'In the form of "price" are letters!'
            return render_template('products_add.html', adding_products_forms=adding_products_forms, error=error)

        if len(customcost) > 5:
            error = 'The number of digits price should not exceed five!'
            return render_template('products_add.html', adding_products_forms=adding_products_forms, error=error)

        import werkzeug.exceptions
        try:

            customimg = request.files['inputFile']  # File storage

        except werkzeug.exceptions.BadRequestKeyError:
            error = 'No picture inserted'
            return render_template('products_add.html', adding_products_forms=adding_products_forms, error=error)

        forms = (customcost, customheadline, customdescription, customtext)

        for form in forms:
            if form == '':
                error = 'One of the form is not filled'
                return render_template('products_add.html', adding_products_forms=adding_products_forms, error=error)

            else:
                img_title = customimg.filename

                import builtins
                try:
                    make_dir_image(customimg, customheadline)
                # This exception occurs due to the fact that we create files in the static folder,
                # saying that the static/ already exists when the product header is empty
                except builtins.FileExistsError:
                    error = 'This headline already exists, or you did not enter a headline'
                    return render_template('products_add.html', adding_products_forms=adding_products_forms,
                                           error=error)

                new_product = Product(headline=customheadline, text=customtext, description=customdescription,
                                      cost=customcost, img_title=img_title, author=current_user.name)

                db.session.add(new_product)
                db.session.commit()

                return redirect(url_for('welcome_page'))

    return render_template('products_add.html', adding_products_forms=adding_products_forms)


@app.route('/cart')
@login_required
def cart_page():

    user_id = current_user.id
    database_cursor.execute("SELECT product.id, product.img_title, product.headline, product.description, product.cost,"
                            "product.slug FROM product, Cart WHERE product.id = Cart.product_id AND Cart.user_id = %s",
                            (user_id, ))

    products = database_cursor.fetchall()

    return render_template('cart_page.html', products=products)


@app.route('/removeFromCart', methods=['GET'])
@login_required
def remove_from_cart():

    if request.method == 'GET':

        product_id = int(request.args.get('product_id'))
        user_id = current_user.id

        database_cursor.execute('DELETE FROM Cart WHERE user_id = %s AND product_id = %s', (user_id, product_id))
        connection_link.commit()

        return render_template('welcome.html')


@app.route('/buyCart', methods=['GET'])
@login_required
def do_buy():

    if request.method == 'GET':
        user_id = current_user.id
        database_cursor.execute('DELETE FROM Cart WHERE user_id = %s', (user_id, ))
        connection_link.commit()

    return render_template('welcome.html')
