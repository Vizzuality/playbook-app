from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os

from routes import routes
from authentication import auth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(routes)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run()
