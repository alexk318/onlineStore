import mysql.connector  # Database driver
from webAppFile import app


class ConfigClass(object):
    DEBUG = True  # Automatic reload of the site when adding new changes to the code

    SECRET_KEY = 'PLEASE DO NOT HACK US'

    from webAppFile import app

    # mysql+driver://Name:Password@IP/DB name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:microlabm666@localhost/onlinestoredb'

    # Responsible for monitoring changes in the database before data is written to it or after data is written
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    SECURITY_PASSWORD_SALT = 'I prefer pepper'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'


dbconfig = app.config['databaseConfig'] = {'host': '127.0.0.1',
                                           'user': 'root',
                                           'password': 'microlabm666',
                                           'database': 'onlinestoredb', }

connection_link = mysql.connector.connect(**dbconfig)
database_cursor = connection_link.cursor()

# database_cursor.execute('''CREATE TABLE Cart
#                        (user_id INTEGER,
#                        product_id INTEGER,
#                        FOREIGN KEY(user_id) REFERENCES user(id),
#                        FOREIGN KEY(product_id) REFERENCES product(id)
#                        )''')


