from flask import Flask
from app.routes import routing

application = Flask(__name__)
application.register_blueprint(routing)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()


