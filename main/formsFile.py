from wtforms import Form, StringField, TextAreaField, PasswordField  # Matching Models with HTML Forms


class RegisterForms(Form):
    nameform = StringField('Name:')
    surnameform = StringField('Surname:')
    emailform = StringField('Email:')
    passwordform = PasswordField('Password:')


class ProductsAddingForms(Form):
    # We can use HTML markup
    headlineform = StringField('Headline: <i>The headline must not exceed 35 characters. The headline should not be '
                               'repeated</i>')
    descriptionform = TextAreaField('Description: ')
    textform = TextAreaField('Text:')
    costform = StringField('Cost:')

