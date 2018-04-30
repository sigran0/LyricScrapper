
from Manager.DriverManager import DriverManager
from Manager.ThreadManager import ThreadManager
from Manager.DatabaseManager import DBM
from Traveler.MelonSongListTraveler import MelonSongListTraveler
from Traveler.MelonRelatedArtistTraveler import MelonRelatedArtistTraveler

class ScrapperManager:

    def __init__(self):
        self.driver_manager = DriverManager()
        self.artist_id_list = []
        self.dbm = DBM()
        self.success_counter = 0
        self.failed_counter = 0

    def start(self, artist_size=1000, start_artist_id=101111):

        print(' > start getting artist id from melon')
        artist_traveler = MelonRelatedArtistTraveler(artist_size)
        self.artist_id_list = artist_traveler.traveling(start_artist_id)
        print(' > complete getting artist id from melon')

        driver = self.driver_manager.run_driver()
        list_traveler = MelonSongListTraveler(driver=driver)

        counter = 0

        for artist_id in self.artist_id_list:
            counter += 1
            datas = list_traveler.traveling(artist_id)

            if datas is None:
                continue

            self.success_counter += datas['success']
            self.failed_counter += datas['fail']

            for data in datas['data']:
                self.dbm.insert(data)
            print(' > [{}/{}]success : {}, fail : {}'.format(counter, len(self.artist_id_list), self.success_counter, self.failed_counter))

        print(' > complete processing, closing driver')
        self.driver_manager.tear_down()