# tfFlask

A simple way to serve your [tensorflow](https://github.com/tensorflow/tensorflow) models with [flask](http://flask.pocoo.org/).

Start a server and run a model:

```python
import tensorflow as tf
from tfFlask import tfFlask

def simple_add():
    x = tf.placeholder(tf.float32, name='x')
    y = tf.placeholder(tf.float32, name='y')
    z = tf.add(x, y, name='z')

tfFlask.register(simple_add)
tfFlask.run()
```

With the server running,

```python
import requests
url = "http://127.0.0.1:5000/feed"
args = {"x":3, "y":4, "target":"z"}
print requests.post(url, json=args).content

# Returns {"z": 7.0}
```