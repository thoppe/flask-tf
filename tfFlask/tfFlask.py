from flask import Flask, request, jsonify, abort
import StringIO, json
import numpy as np

_MODEL = None
def register(model):
    global _MODEL
    from tfModel import tfModel
    _MODEL = tfModel(model)

#################################################################

def numpy_unpack(serialized):
    memfile = StringIO.StringIO()
    memfile.write(serialized)
    memfile.seek(0)
    return np.load(memfile)

#################################################################



app = Flask(__name__)

@app.route('/')
def index():
    msg = '''Endpoints:\n/feed'''
    return msg.strip()

@app.route('/check', methods=['POST'])
def check():
    global _MODEL
    
    js = request.json
    if not js: abort(400)

    data = {}
    for name in js:
        data[name] =  _MODEL.get_info(name)
        
    return jsonify(data), 200

@app.route('/serve', methods=['POST'])
def process():
    global _MODEL
    assert(_MODEL is not None)

    print vars(request)

    feed_args = {}
    for k,v in request.files.items():
        feed_args[k] = numpy_unpack(v.read())
    print feed_args  
    #js = request.json
    #if not js: abort(400)

    #target = js.pop('target')
    #result = _MODEL(target, **js)
    #return jsonify({target:result}), 200
    return jsonify({}), 200
    

def run():
    app.run(debug=True)

if __name__ == "__main__":

    import tensorflow as tf
    def scalar_add():
        x = tf.placeholder(tf.float32)
        y = tf.placeholder(tf.float32)
        z = tf.add(x, y)
        return {'x':x, 'y':y, 'z':z}

    def L2norm():
        x = tf.placeholder(tf.float32, shape=(None,))
        return {'x':x, 'z':tf.norm(x)}

    register(L2norm)
    run()

