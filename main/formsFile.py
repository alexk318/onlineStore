from wtforms import Form, StringField, TextAreaField, PasswordField  # Matching Models with HTML Forms


class RegisterForms(Form):
    nameform = StringField('Name:')
    surnameform = StringField('Surname:')
    emailform = StringField('Email:')
    passwordform = PasswordField('Password:')


class ProductForms(Form):
    # We can use HTML markup
    headlineform = StringField('Headline:',render_kw={'maxlength': 35,
                                                      'placeholder': 'The headline must not exceed 35 characters',
                                                      'required': True})

    descriptionform = StringField('Description:',
                                  render_kw={'maxlength': 50, 'placeholder': 'The description must not exceed 50 '
                                                                             'characters', 'required': True})
    textform = TextAreaField('Text:', render_kw={'required': True})
    costform = StringField('Cost:', render_kw={'maxlength': 5, 'placeholder': 'Maximum number of digits - 5',
                                               'required': True})

    # regforms stores all RegisterForm class arguments
regforms = RegisterForms()
productforms = ProductForms()
