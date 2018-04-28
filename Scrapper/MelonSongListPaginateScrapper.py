from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from Scrapper.Scrapper import Scrapper


class MelonSongListPaginateScrapper(Scrapper):

    def __init__(self, driver):
        Scrapper.__init__(self)

        self.artist_id = 228069
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

            if len(args) != 1:
                raise ValueError('scrapping(artist_id) -> args must have just one item')

            artist_id = args[0]

            self.set_url(artist_id, 1)

            self.driver.get(self.url)
            try:
                # get page_len
                print(' > waiting for loading paginate')
                self.driver.implicitly_wait(3)
                res = WebDriverWait(self.driver, 10)\
                    .until(EC.presence_of_element_located((By.ID, 'pageObjNavgation')))

                html = res.get_attribute('innerHTML')

                soup = BeautifulSoup(html, 'html.parser')

                span = soup.select('div > span')

                if len(span) <= 0:
                    return None

                span = span[0]

                page_list = span.findChildren()
                return len(page_list) - 1

            except TimeoutException:
                print('loading took too much time')
