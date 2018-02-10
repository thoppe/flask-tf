from server import app
from default_caller import MODEL


def serve(model_function, debug=True):
    MODEL.set_model(model_function)
    app.run(debug=debug)
