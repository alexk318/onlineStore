from flask import render_template, session, request, redirect, url_for
from flask_security import login_required, current_user
from formsFile import regforms, productforms
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
    dirstr = "main/static/imgs" + foldername
    os.makedirs(dirstr)  # Creating a folder
    write_file(fileimage.read(), dirstr + "/" + img_title)


@app.route('/')
def welcome_page():  # Define the 'View'
    # The use of tags is adequately perceived, but better to use HTML templates
    return render_template('welcome.html')

@app.route('/registration', methods=['POST', 'GET'])
def registration_page():

    # Web server accepts data
    if request.method == 'POST':
        nameuser = request.form['nameform']
        surnameuser = request.form['surnameform']
        emailuser = request.form['emailform']
        passworduser = request.form['passwordform']

        new_user = user_datastore.create_user(name=nameuser, surname=surnameuser, email=emailuser,
                                              password=passworduser)

        # Adding values to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('welcome_page'))

    return render_template('registration.html', regforms=regforms)


@app.route('/sell', methods=['POST', 'GET'])
@login_required
def add_page():
    if request.method == 'POST':
        customheadline = request.form['headlineform']
        customdescription = request.form['descriptionform']
        customimg = request.files['inputFile']  # File storage
        customcost = request.form['costform']
        customtext = request.form['textform']

        forms = (customheadline, customdescription, customimg, customcost, customtext)

        img_title = customimg.filename

        if not img_title.lower().endswith(('.png', '.jpg', '.jpeg', '.jpe')):
            error = 'Valid extensions for photos: ".png, .jpg, .jpeg, .jpe"'
            return render_template('products_add.html', adding_products_forms=adding_products_forms, error=error)
        else:
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

    return render_template('products_add.html', productforms=productforms)


@app.route('/cart')
@login_required
def cart_page():
    database_cursor.execute("SELECT product.id, product.img_title, product.headline, product.description, product.cost,"
                            "product.slug FROM product, Cart WHERE product.id = Cart.product_id AND Cart.user_id = %s",
                            (current_user.id,))

    cart_products = database_cursor.fetchall()

    return render_template('cart_page.html', cart_products=cart_products)


@app.route('/buyCart', methods=['GET'])
@login_required
def do_buy():

    if request.method == 'GET':

        database_cursor.execute(
            "SELECT product.id FROM product, Cart WHERE product.id = Cart.product_id AND Cart.user_id = %s",
            (current_user.id,))

        products = database_cursor.fetchall()

        for everyproduct in products:
            database_cursor.execute("UPDATE product SET product.slug = NULL WHERE product.id = %s", (everyproduct[0], ))
            connection_link.commit()

        database_cursor.execute("DELETE FROM Cart WHERE user_id = %s", (current_user.id, ))
        connection_link.commit()

    return redirect(url_for('welcome_page'))


@app.route('/removeFromCart', methods=['GET'])
@login_required
def remove_from_cart():
    if request.method == 'GET':

        product_id = int(request.args.get('product_id'))

        database_cursor.execute('UPDATE product SET product.visible = True Where product.id = %s', (product_id, ))
        connection_link.commit()

        database_cursor.execute('DELETE FROM Cart WHERE user_id = %s AND product_id = %s', (current_user.id, product_id))
        connection_link.commit()

        message_success = 'Product successfully removed from the cart'
        return render_template('message.html', message_success=message_success)


@app.errorhandler(404)
def handler_404(err):
    message_alert = 'You have moved to a non-existent page'
    return render_template('message.html', message_alert=message_alert), 404
