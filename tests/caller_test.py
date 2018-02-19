from flasktf import caller
import numpy as np
from nose.tools import assert_equal
import subprocess
import time
import signal
import os

startup_time = 4.0


class Caller_Test:

    @classmethod
    def setup_class(cls):
        print("Starting tiny server")
        cls.P = subprocess.Popen(["python", "tests/tiny_server.py"])
        time.sleep(startup_time)
        cls.model = caller()

    @classmethod
    def teardown_class(cls):
        os.kill(cls.P.pid, signal.SIGINT)
        time.sleep(1)

    def call_empty_info_test(self):
        output = self.model.info()
        expected = ['x', 'z']
        assert_equal(output, expected)

    def call_info_test(self):
        output = self.model.info('x')
        expected = {"x": {"dtype": "<dtype: 'float32'>", "rank": 1}}
        assert_equal(output, expected)

    def call_model_L2(self):
        x = np.random.uniform(size=(50,))
        output = self.model('z', x=x)['z']

        np.testing.assert_array_almost_equal(
            output,
            np.linalg.norm(x),
            decimal=5,
        )
