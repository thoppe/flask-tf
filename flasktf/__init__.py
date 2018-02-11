from server import app
from caller import caller


def serve(
        model_function,
        port=None,
        debug=True):  # pragma: no cover

    from default_caller import MODEL
    MODEL.set_model(model_function)
    app.run(debug=debug, port=port)

__all__ = [
    "caller",
    "app",
]
