from flask import Flask, request, jsonify, abort
from default_caller import MODEL

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
