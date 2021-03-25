import connexion

# Pieces of generated code
from .encoder import JSONEncoder
from odd_contract.controllers import ODDController, ControllerHolder


def init_flask_app(controller: ODDController):
    app = connexion.App(__name__, specification_dir='openapi')
    app.add_api(specification='openapi.yaml',
                arguments={'title': 'ODD adapter HTTP API contract'},
                pythonic_params=True)

    ControllerHolder.init_controller(controller)

    app = app.app
    app.json_encoder = JSONEncoder
    return app
