import os

import connexion
from flask import Response
from flask_compress import Compress
# Pieces of generated code
from odd_models.adapter.controllers import ODDController, ControllerHolder


def init_flask_app():
    app = connexion.App(__name__, specification_dir='openapi')
    app.add_api(specification='openapi.yaml',
                arguments={'title': 'ODD adapter HTTP API contract'},
                pythonic_params=True)

    app = app.app
    app.add_url_rule(os.environ.get('HEALTHCHECK_PATH', '/health'), "healthcheck", lambda: Response(status=200))
    Compress().init_app(app)
    return app


def init_controller(controller: ODDController):
    ControllerHolder.init_controller(controller)
