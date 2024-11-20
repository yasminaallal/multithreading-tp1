import unittest
from task import Task
import numpy.testing as npt
import numpy as np


class TestTask(unittest.TestCase):
    def test_work(self):
        task = Task()
        task.work()
        npt.assert_allclose(
            np.dot(task.a, task.x),
            task.b,
            rtol=1e-5,
            atol=1e-8,
            err_msg="The solution does not satisfy A * x = b",
        )


if __name__ == "__main__":
    unittest.main()
