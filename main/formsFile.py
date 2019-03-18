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
    descriptionform = StringField('Description: <i>The description must not exceed 50 characters</i>')
    textform = TextAreaField('Text:')
    costform = StringField('Cost: <i>Maximum number of digits - 5</i>')

