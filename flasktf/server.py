from flask import Flask, request, jsonify
from default_caller import MODEL
from serializers import pack, unpack

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    endpoints = ['info', 'serve']
    return jsonify(endpoints), 200


@app.route('/info', methods=['POST'])
def info():
    js = request.json
    if not js:
        return jsonify(MODEL.get_variables().keys()), 200

    data = {}
    for name in js:
        data[name] = MODEL.get_info(name)

    return jsonify(data), 200


@app.route('/call', methods=['POST'])
def call():
    assert(MODEL is not None)

    feed_args = {}
    targets = None

    for k, v in request.files.items():
        if k != "_targets":
            feed_args[k] = unpack(v.read())
        else:
            targets = unpack(v.read())

    assert(targets is not None)

    result = MODEL(*targets, **feed_args)
    serialized = pack(result)

    return serialized, 200


def run():
    app.run(debug=True)
