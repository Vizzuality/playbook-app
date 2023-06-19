from flask import Flask
import logging
from dotenv import load_dotenv
import os

from index_builder import IndexBuilder
from routes import routes
from authentication import auth

load_dotenv()
logging.basicConfig(level=logging.INFO)  # Set the desired log level

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(routes)
app.register_blueprint(auth)


@app.before_request
def initialize():
    if not app.config.get('initialized'):
        app.logger.info("Initializing content...")
        IndexBuilder()
        app.config['initialized'] = True
        app.logger.info("Content initialization complete.")


if __name__ == "__main__":
    app.run()
