from webAppFile import app
from blueprintFile import blueprint_instance

import viewFile  # Start Page Display

# Pass an instance of the Blueprint class, Blueprint Homepage
app.register_blueprint(blueprint_instance, url_prefix='/buy')

if __name__ == '__main__':
    app.run()
