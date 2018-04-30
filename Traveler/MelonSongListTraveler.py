
from Scrapper.MelonSongListPaginateScrapper import MelonSongListPaginateScrapper
from Scrapper.MelonSongListScrapper import MelonSongListScrapper

from Traveler.Traveler import Traveler

from Manager.ThreadManager import ThreadManager


class MelonSongListTraveler(Traveler):

    def __init__(self, driver):

        Traveler.__init__(self)

        self.artist_id = 0
        self.index = 1
        self.page_num = 1
        self.page_len = 0

        self.url =  'https://www.melon.com/artist/song.htm?artistId={}' \
                    '#params[listType]=A&params[orderBy]=ISSUE_DATE&params[artistId]={}&po=pageObj&startIndex={}'\
                    .format(self.artist_id, self.artist_id, self.index)
        self.driver = driver

    def traveling(self, artist_id):
        print(' > artist_id {} start'.format(artist_id))
        self.artist_id = artist_id
        paginate_scrapper = MelonSongListPaginateScrapper(self.driver)

        self.artist_id = artist_id
        self.page_len = paginate_scrapper.scrapping(self.artist_id)

        if self.page_len is None:
            return None

        list_scrapper = MelonSongListScrapper(self.driver)

        result = dict()
        result['data'] = []

        success_counter = 0
        failed_counter = 0

        for index in range(1, self.page_len * 50, 50):
            print(' > {} [{}/{}], waiting for loading song list'.format(self.artist_id, int(index / 50) + 1, self.page_len))
            datas = list_scrapper.scrapping(self.artist_id, index)

            success_counter += datas['success']
            failed_counter += datas['fail']

            for data in datas['data']:
                result['data'].append(data)

        result['success'] = success_counter
        result['fail'] = failed_counter

        print(' > artist_id {} end'.format(artist_id))

        return result
