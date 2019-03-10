from webAppFile import app
from blueprintFile import blueprint_instance

import viewFile  # Start Page Display

# Pass an instance of the Blueprint class, Blueprint Homepage
app.register_blueprint(blueprint_instance, url_prefix='/buy')

# If the interpreter starts some module (source file) as the main program, it assigns the special variable __name__
# the value "__main__". If this file is imported from another module, the variable __name__
# will be assigned the name of this module.
if __name__ == '__main__':
    app.run()

