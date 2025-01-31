from multiprocessing.managers import BaseManager
from queue import Queue

#  herite base manager
#  ouvrie un server sur le port avec mot de passe
#  fourni des accesseur aux task queue et result queue


class QueueManager(BaseManager):
    pass


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000
    AUTHKEY = b"secret"

    task_queue = Queue()
    result_queue = Queue()

    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)

    manager = QueueManager(address=(HOST, PORT), authkey=AUTHKEY)
    server = manager.get_server()
    print(f"Server started on {HOST}:{PORT}")
    server.serve_forever()

#  Queue Client

#  travail se connecter aux serveurs partage port et mdp avec Queue MAneger
# lance serveur ouvre port et on attend


class QueueClient:
    def __init__(self, host, port, authkey):
        QueueManager.register("get_task_queue")
        QueueManager.register("get_result_queue")
        manager = QueueManager(address=(host, port), authkey=authkey)
        manager.connect()

        self.task_queue = manager.get_task_queue()
        self.result_queue = manager.get_result_queue()
