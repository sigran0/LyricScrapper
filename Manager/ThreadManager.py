import code
from Manager.DataManager import DataManager
from threading import Thread


class ThreadManager:

    def __init__(self, data, max_threads_size=5):
        self.max_threads_size = max_threads_size
        self.data_manager = DataManager(data, max_threads_size)

    def create_threads(self, target_method):
        threads = []

        _code, data_list = self.data_manager.get_item_list()

        if len(data_list) > 0:
            for c, data in enumerate(data_list):
                thread_id = 'thread-{}'.format(c)
                thread = Thread(target=target_method, args=(thread_id, data))
                threads.append(thread)
        return _code, threads

    def start_threads(self, target_method):

        count = 0
        while True:
            count += 1
            #print(' > [{}] start'.format(count))
            _code, threads = self.create_threads(target_method)

            if len(threads) > 0:
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(15)

            #print(' > [{}] end'.format(count))

            if _code is code.EMPTY:
                break
