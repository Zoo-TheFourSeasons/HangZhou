# -*- coding: utf-8 -*-
"""app
"""
from flask import Flask

from extensions import register_ext
from configuration.read import app_config


def create_app():
    """create app
    """
    app = Flask(__name__)
    app.debug = True
    app.secret_key = app_config['app']['secret-key']
    app.config.update(WTF_CSRF_SECRET_KEY=app_config['app']['secret-key'],
                      WTF_CSRF_TIME_LIMIT=int(app_config['app']['csrf-time']),
                      WTF_CSRF_ENABLED=app_config['app'].getboolean('csrf-enable'),

                      PERMANENT_SESSION_LIFETIME=int(app_config['app']['session-time']),
                      SESSION_REFRESH_EACH_REQUEST=app_config['app'].getboolean('session-refresh'),

                      SEND_FILE_MAX_AGE_DEFAULT=int(app_config['app']['max-age']),
                      FLASK_DB_QUERY_TIMEOUT=float(app_config['app']['query-time']))
    register_ext(app)

    return app


app_ = create_app()
