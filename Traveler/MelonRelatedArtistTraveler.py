import random
from Scrapper.MelonRelatedArtistScrapper import MelonRelatedArtistScrapper
from Traveler.Traveler import Traveler


class MelonRelatedArtistTraveler(Traveler):

    def __init__(self, max_size):
        Traveler.__init__(self)

        self.untraveled_dict = dict()
        self.traveled_dict = dict()
        self.traveled_len = 0
        self.scrapper = MelonRelatedArtistScrapper()
        self.max_size = max_size

        if self.max_size <= 0:
            raise ValueError('max_size must bigger than 0')

    def traveling(self, artist_id):

        artist_id = str(artist_id)

        print(' > process {}, {} items remained, {} items completed'.format(artist_id, len(self.untraveled_dict), self.traveled_len))
        ids = self.scrapper.scrapping(artist_id)
        self.traveled_len = len(self.traveled_dict)
        self.untraveled_dict[artist_id] = True

        self.dictionarization(artist_id, ids)

        _next = random.choice(list(self.untraveled_dict))

        if self.traveled_len <= self.max_size:
            self.traveling(_next)
            return [*self.traveled_dict]

    def dictionarization(self, artist_id, ids):

        if ids is not None:
            if len(ids) > 0:
                for _id in ids:
                    if self.traveled_dict.get(_id) is None:
                        self.untraveled_dict[_id] = True
        self.untraveled_dict.pop(artist_id)
        self.traveled_dict[artist_id] = True
