from flask import Flask, redirect, url_for  # Web-framework

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_migrate import Migrate, MigrateCommand  # Changing database structure in an adequate way

from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy  # Associating a database with object-oriented programming language concepts

from flask_security import SQLAlchemyUserDatastore, Security, current_user

# __name__ is set to the name of the current class, function, method, descriptor, or generator instance.
app = Flask(__name__, static_url_path="/static")

from configurationFile import ConfigClass  # Moved to correctly import 'app' into configurationFile

app.config.from_object(ConfigClass)  # Passing application settings through a method from_object

db = SQLAlchemy(app)  # Create a instance of the SQLALCHEMY

migrate = Migrate(app, db)

manager = Manager(app)  # Controller class for handling a set of commands
manager.add_command('dbcommand', MigrateCommand)  # Command for migrate

from modelsFile import *
# SETTING UP THE ADMIN #

# Override methods for restricting login to admin panel


class AdminView(ModelView):  # AdminView - custom name
    def is_accessible(self) -> bool:  # Availability check
        return current_user.has_role('Administrator')

    def inaccessible_callback(self, name, **kwargs):  # Check for unavailability
        return redirect(url_for('welcome_page'))


admin = Admin(app, 'Admin Panel', url='/admin')
admin.add_view(AdminView(User, db.session))  # Adding models to the admin panel
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Product, db.session))

# FLASK-SECURITY #

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)  # Connect Flask-Security to the application
