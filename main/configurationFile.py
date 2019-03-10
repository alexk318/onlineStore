import mysql.connector  # Database driver


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

    app.config['databaseConfig'] = {'host': '127.0.0.1',
                                    'user': 'root',
                                    'password': 'microlabm666',
                                    'database': 'onlinestoredb'}


class UsingDataBase:  # All necessary database settings are stored in this class.
    def __init__(self, config: dict) -> None:  # Before performance
        self.configuration = config

    def __enter__(self):  # Run at startup
        self.connectionLink = mysql.connector.connect(**self.configuration)
        self.databaseCursor = self.connectionLink.cursor()

        return self.databaseCursor

    def __exit__(self) -> None:  # After performance
        self.connectionLink.commit()  # Record all changes
        self.databaseCursor.close()
        self.connectionLink.close()


