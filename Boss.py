from task import Task
from QueueManager import QueueClient
# task queue . put ( work
# ) dans une une boucle from django.conf import settings
# apres on recupere aussi dans une boucle for result queue
# recupere des accesseurs pour acceder a taskqueue``


class Boss(QueueClient):
    def __init__(self, host, port, authkey, num_tasks):
        super().__init__(host, port, authkey)
        self.num_tasks = num_tasks

    def execute(self):
        for i in range(self.num_tasks):
            task = Task(identifier=i)
            print(f"Boss: Adding {task}")
            self.task_queue.put(task)

        print("Boss: Waiting for results...")
        for _ in range(self.num_tasks):
            result = self.result_queue.get()
            print(f"Boss: Received result for {result}")


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000
    AUTHKEY = b"secret"

    client = Boss(HOST, PORT, AUTHKEY, num_tasks=5)
    client.execute()
