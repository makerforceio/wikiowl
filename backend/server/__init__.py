import os
import uuid
import json

from flask import Flask
from flask import request

from server.db import get_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'wikiowl.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Injecting the database
    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/token', methods=['GET'])
    def token_generate():
        return str(uuid.uuid4())

    @app.route('/link/<token>', methods=['POST'])
    def add_link(token):
        db = get_db()

        # Retrieve the link
        body = request.json

        db.execute('INSERT INTO history (person_token, link) VALUES (?, ?)', (token, body["link"]))
        db.commit()

        return "Success"

    return app
