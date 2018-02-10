from server import app
from default_caller import MODEL
from caller import caller


def serve(model_function, debug=True):
    MODEL.set_model(model_function)
    app.run(debug=debug)

__all__ = [
    "caller",
]
