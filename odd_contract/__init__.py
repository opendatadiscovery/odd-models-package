import connexion

# Piece of generated code
from .encoder import JSONEncoder


def init_flask_app():
    app = connexion.App(__name__, specification_dir='openapi')
    app.add_api(specification='openapi.yaml',
                arguments={'title': 'ODD adapter HTTP API contract'},
                pythonic_params=True)

    app = app.app
    app.json_encoder = JSONEncoder
    return app
