from flasktf import app, caller
from flasktf.default_caller import MODEL
from nose.tools import assert_equal
import json
import tensorflow as tf


class Serializer_Test:

    @classmethod
    def setup_class(cls):

        def model():
            x = tf.placeholder(tf.float32, shape=(None,))
            return {'x': x, 'z': tf.norm(x)}

        MODEL.set_model(model)

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.caller = caller()

    def call_endpoint_test(self):
        output = self.app.get('/').get_data()
        expected = ['info', 'serve']
        assert_equal(json.loads(output), expected)

    def call_empty_info_test(self):
        output = self.app.post('/info').get_data()
        expected = ['x', 'z']
        assert_equal(json.loads(output), expected)

    def call_info_test(self):
        output = self.app.post(
            '/info',
            data=json.dumps(['x']),
            content_type='application/json',
        )

        processed = json.loads(output.get_data())
        expected = {"x": {"dtype": "<dtype: 'float32'>", "rank": 1}}
        assert_equal(processed, expected)
