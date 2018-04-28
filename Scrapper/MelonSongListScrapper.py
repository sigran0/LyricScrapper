import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from Scrapper.MelonLyricScrapper import MelonLyricScrapper
import utils

from Scrapper.Scrapper import Scrapper


class MelonSongListScrapper(Scrapper):

    def __init__(self, driver):
        Scrapper.__init__(self)

        self.artist_id = 0
        self.index = 1
        self.url =  'https://www.melon.com/artist/song.htm?artistId={}' \
                    '#params[listType]=A&params[orderBy]=ISSUE_DATE&params[artistId]={}&po=pageObj&startIndex={}'\
                    .format(self.artist_id, self.artist_id, self.index)
        self.driver = driver

    def set_url(self, *args):
        if len(args) != 2:
            raise ValueError('set_url(artist_id, index) -> args must have just two item')

        self.artist_id = args[0]
        self.index = args[1]
        self.url =  'https://www.melon.com/artist/song.htm?artistId={}' \
                    '#params[listType]=A&params[orderBy]=ISSUE_DATE&params[artistId]={}&po=pageObj&startIndex={}'\
                    .format(self.artist_id, self.artist_id, self.index)

    def scrapping(self, *args):
        if self.driver is not None:

            if len(args) != 2:
                raise ValueError('scrapping(artist_id, index) -> args must have just two item')

            self.artist_id = args[0]
            index = args[1]

            self.set_url(self.artist_id, index)
            self.driver.get(self.url)

            result = dict()
            result['data'] = []

            try:
                time.sleep(1)
                res = WebDriverWait(self.driver, 10)\
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, '#frm')))

                html = res.get_attribute('innerHTML')

                soup = BeautifulSoup(html, 'html.parser')

                a = soup.select('td > div > div > a.btn.btn_icon_detail')

                success_counter = 0
                failed_counter = 0

                for data in a:
                    song_data = {}
                    song_data['artist_id'] = self.artist_id
                    song_data['song_id'] = utils.extract_numbers(data['href'])[0]

                    scrapper = MelonLyricScrapper()
                    song_data['song_info'] = scrapper.scrapping(song_data['song_id'])

                    if song_data['song_info'] is None:
                        failed_counter += 1
                        continue

                    success_counter += 1
                    result['data'].append(song_data)
                result['success'] = success_counter
                result['fail'] = failed_counter

                return result

            except TimeoutException:
                print('loading took too much time')
