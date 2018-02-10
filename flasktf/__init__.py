from server import app
from caller import caller


def serve(model_function, debug=True):
    from default_caller import MODEL
    MODEL.set_model(model_function)
    app.run(debug=debug)

__all__ = [
    "caller",
    "app",
]
