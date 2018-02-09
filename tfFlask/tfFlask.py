from flask import Flask, request, jsonify, abort
import StringIO, json
import numpy as np
import requests
import json

#################################################################

class tfFlask(object):
    def __init__(self):
        self.url = "http://127.0.0.1:5000/"

    def check(self, *args):
        url = self.url + 'check'
        r = requests.post(url, json=args)
        return json.loads(r.content)

    def serve(self, *targets, **feed_dict):
        url = self.url + 'serve'
        files = {'_targets':numpy_pack(targets)}
        for k,v in feed_dict.items():
            files[k] = numpy_pack(v)
            
        r = requests.post(url, files=files)
        return numpy_unpack(r.content)


#################################################################

_MODEL = None

def register(model):
    global _MODEL
    from tfModel import tfModel
    _MODEL = tfModel(model)

def numpy_unpack(serialized):
    memfile = StringIO.StringIO()
    memfile.write(serialized)
    memfile.seek(0)
    return np.load(memfile)

def numpy_pack(x):
    memfile = StringIO.StringIO()
    np.save(memfile, x)
    memfile.seek(0)
    return memfile.read()


#################################################################

app = Flask(__name__)

@app.route('/')
def index():
    msg = '''Endpoints:\n/check\nserve'''
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
    targets = None
    
    for k,v in request.files.items():
        if k != "_targets":
            feed_args[k] = numpy_unpack(v.read())
        else:
            targets = numpy_unpack(v.read())

    assert(targets is not None)

    result = _MODEL(*targets, **feed_args)
    serialized = numpy_pack(result)

    return serialized, 200
    

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

