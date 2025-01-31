import time
import numpy as np
import json


class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        self.size = size or np.random.randint(300, 3_000)
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def __str__(self):
        return f"Task {self.identifier}"

    @staticmethod
    def from_json(json_text: str) -> "Task":
        data = json.loads(json_text)
        task = Task(identifier=data.get("identifier", 0), size=data.get("size"))
        task.time = data.get("time", 0)
        task.x = np.array(data.get("x", np.zeros((task.size,))))
        task.a = np.array(data.get("a", np.random.rand(task.size, task.size)))
        task.b = np.array(data.get("b", np.random.rand(task.size)))
        return task

    def to_json(self) -> str:
        data = {
            "identifier": self.identifier,
            "size": self.size,
            "time": self.time,
            "x": self.x.tolist(),
            "a": self.a.tolist(),
            "b": self.b.tolist(),
        }
        return json.dumps(data)

    def __eq__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return False
        return (
            self.identifier == other.identifier
            and self.size == other.size
            and np.array_equal(self.a, other.a)
            and np.array_equal(self.b, other.b)
            and np.array_equal(self.x, other.x)
            and self.time == other.time
        )
