from pymongo import MongoClient

class DBM:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.lyricdb
        self.song_datas = self.db.song_data

    def insert(self, data):
        try:
            self.song_datas.insert(data)
        except:
            print('insert failed')