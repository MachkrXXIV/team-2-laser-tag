import threading


class GracefulThread(threading.Thread):
    """
    Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self, *args, **kwargs):
        super(GracefulThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        print("Thread stopping")
        self._stop_event.set()

    def stopped(self):
        print("Thread stopped")
        return self._stop_event.is_set()
