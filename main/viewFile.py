# Flask and Django use pattern MVC:
# Model - Model Description (db)
# View - Data mapping to user
# Controller - Binds user and database, app

from flask import render_template, send_from_directory  # 'render_template' displays HTML to the page
from flask import request, redirect, url_for

from flask_security import login_required

from formsFile import RegisterForms, ProductsAddingForms

from webAppFile import app, db, user_datastore

from modelsFile import Product

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


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():

    # Web server accepts data
    if request.method == 'POST':
        # We request forms from the RegisterForm class by writing them into separate variables.
        nameuser = request.form['nameform']
        surnameuser = request.form['surnameform']
        emailuser = request.form['emailform']
        passworduser = request.form['passwordform']

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
    if request.method == 'POST':
        customheadline = request.form['headlineform']
        customtext = request.form['textform']
        customdescription = request.form['descriptionform']
        customcost = request.form['costform']
        customimg = request.files['inputFile']  # File storage

        img_title = customimg.filename

        make_dir_image(customimg, customheadline)

        new_product = Product(headline=customheadline, text=customtext, description=customdescription,
                                  cost=customcost, img_title=img_title)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('welcome_page'))

    adding_products_forms = ProductsAddingForms()
    return render_template('products_add.html', adding_products_forms=adding_products_forms)

