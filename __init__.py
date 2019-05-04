import os
from flask import Flask, request, g, jsonify, Response
from flask_api import status
import sqlite3
from dotenv import load_dotenv
from flask_sqlite_api.db import get_db, close_db, to_json

load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'secret_key'
    app.logger.info("Creating app")

    @app.route('/', methods=['GET'])
    def index():
        db = get_db()
        posts = db.execute(
            'SELECT * FROM posts'
        ).fetchall()
        # app.logger.info(posts)
        return to_json(posts)

    @app.route('/', methods=['POST'])
    def create():
        post = request.get_json(silent=True)

        title = post.get('title', None)
        body = post.get('body', None)

        error = None

        if not title:
            error = 'title is required.'

        if error is not None:
            return jsonify({"error": error}), status.HTTP_400_BAD_REQUEST
        else:
            db = get_db()
            db.execute(
                'INSERT INTO posts (title, body)'
                ' VALUES (?, ?)',
                (title, body)
            )
            db.commit()
            return 'success'

    @app.teardown_appcontext
    def close_connection(exception):
        close_db()

    return app
