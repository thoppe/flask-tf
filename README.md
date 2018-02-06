# tfFlask

A simple way to serve your tensorflow models with flask.

```
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

```
import requests
url = "http://127.0.0.1:5000/feed"
args = {"x":3, "y":4, "target":"z"}
print requests.post(url, json=args).content

# Returns {"z": 7.0}
```