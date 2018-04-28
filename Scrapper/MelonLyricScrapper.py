
import requests
import re
import datetime
from bs4 import BeautifulSoup
from Scrapper.Scrapper import Scrapper


class MelonLyricScrapper(Scrapper):

    def __init__(self):
        Scrapper.__init__(self)
        self.url = 'https://www.melon.com/song/detail.htm?songid='

    def strip_html(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def strip_19(self, data):
        p = re.compile(r'(19금|\r|\n|\t)')
        return p.sub('', data)

    def find_hanguel(self, data):
        mat = re.match(r'.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', data)

        if mat is None:
            return False
        else:
            return True

    def set_url(self, *args):
        if len(args) != 1:
            raise ValueError('set_url(song_id) -> args must have just one item')
        self.url = 'https://www.melon.com/song/detail.htm?songid={}'.format(args[0])

    def scrapping(self, *args):

        if len(args) != 1:
            raise ValueError('scrapping(song_id) -> args must have just one item')

        song_id = args[0]

        self.set_url(song_id)
        result = {}

        try:
            req = requests.get(self.url)
            html = req.text

            soup = BeautifulSoup(html, 'html.parser')

            lyric_data = soup.select('#d_video_summary')
            lyric_data = str(lyric_data[0]).replace('<br/>', '\n')
            lyric_data = self.strip_html(lyric_data)
            lyric_data = lyric_data.strip()

            if self.find_hanguel(lyric_data) is False:
                return None

            title_data = soup.select('#downloadfrm > div > div > div.entry > div.info > div.song_name')
            title_data = self.strip_19(title_data[0].text[4:].strip())

            artist_data = soup.select(
                '#downloadfrm > div > div > div.entry > div.info > div.artist > a > span:nth-of-type(1)')
            artist_data = self.strip_html(str(artist_data[0]))

            meta_datas = soup.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd')

            result['artist'] = artist_data
            result['title'] = title_data
            result['album'] = meta_datas[0].text
            result['release_date'] = datetime.datetime.strptime(meta_datas[1].text, '%Y.%m.%d').timestamp()
            result['genre'] = meta_datas[2].text
            result['lyric'] = lyric_data

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
            # print(self.emit_error_message() % (song_id))
            return None
        except ValueError as e:
            return None
