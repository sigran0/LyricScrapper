
import requests
from bs4 import BeautifulSoup

import utils
from Scrapper.Scrapper import Scrapper


class MelonRelatedArtistScrapper(Scrapper):

    def __init__(self):
        Scrapper.__init__(self)
        self.target_index = 0
        self.url = 'https://www.melon.com/artist/detail.htm?artistId='

    def set_url(self, *args):
        if len(args) != 1:
            raise ValueError('set_url(song_id) -> args must have just one item')

        self.url = 'https://www.melon.com/artist/detail.htm?artistId={}'.format(args[0])

    def scrapping(self, *args):

        if len(args) != 1:
            raise ValueError('scrapping(artist_id) -> args must have just one item')

        artist_id = args[0]

        self.set_url(artist_id)
        try:
            req = requests.get(self.url)
            html = req.text

            soup = BeautifulSoup(html, 'html.parser')
            wrap_list = soup.select('#conts > div.section_atistinfo06.d_artist_list > div > div.wrap_list')

            result = set()

            for wrap in wrap_list:
                gubun_object = wrap.select('ul > li > div > div > dl > dd.gubun')
                a_list = wrap.select('ul > li > div > div > dl > dt > a')

                for c, a in enumerate(a_list):
                    gubun_string = gubun_object[c].text.strip()
                    gubuns = gubun_string.split('/')

                    if len(gubuns) > 2:
                        region = gubuns[0]
                        sex = gubuns[1]
                        group_type = gubuns[2]

                        if region == '대한민국':
                            _artist_id = utils.extract_numbers(a['href'])[0]
                            # print(_artist_id, region, sex, group_type)
                            result.add(_artist_id)

            return result
        except requests.exceptions.Timeout as e:
            # print(self.emit_error_message() % (song_id))
            return None
        except requests.exceptions.TooManyRedirects as e:
            # print(self.emit_error_message() % (song_id))
            return None
        except requests.exceptions.RequestException as e:
            # print(self.emit_error_message() % (song_id))
            return None
        except IndexError as e:
            #print(self.emit_error_message() % (song_id))
            return None
