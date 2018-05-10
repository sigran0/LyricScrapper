from Manager.RequestManager import RequestManager


class DBM:

    def __init__(self):
        self.request_manager = RequestManager()

    def insert_song(self, data):
        self.request_manager.set_target_url('songs')
        result = self.request_manager.post(data)

        return result
