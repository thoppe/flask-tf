from server import app
from caller import caller

from default_caller import MODEL

def serve(model_function, debug=True):
    MODEL.set_model(model_function)
    app.run(debug=debug)

