from wtforms import Form, StringField, TextAreaField, PasswordField  # Matching Models with HTML Forms


class RegisterForms(Form):
    nameform = StringField('Name:')
    surnameform = StringField('Surname:')
    emailform = StringField('Email:')
    passwordform = PasswordField('Password:')


class ProductsAddingForms(Form):
    headlineform = StringField('Headline:')
    descriptionform = TextAreaField('Description: ')
    textform = TextAreaField('Text:')
    costform = StringField('Cost:')

