import server
from caller import tfCaller, kerasCaller
from model_session import tfModelSession, kerasModelSession

def serveTF(
        model_function,
        port=None,
        debug=True):  # pragma: no cover

    server.MODEL = tfModelSession()
    server.MODEL.set_model(model_function)
    server.app.run(debug=debug, port=port)

def serveKeras(
        model_function,
        port=None,
        debug=True,
        *args, **kwargs
):  # pragma: no cover

    server.MODEL = kerasModelSession()
    server.MODEL.set_model(model_function, *args, **kwargs)
    server.app.run(debug=debug, port=port)

__all__ = [
    "tfCaller",
    "kerasCaller",
    "app",
]
