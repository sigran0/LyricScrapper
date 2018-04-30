
import code


class DataContainer:

    def __init__(self, data):

        if type(data) is list:
            self.coroutine = self.call_coroutine(data)
        else:
            self.coroutine = None
            raise ValueError('DataContainer(data) -> argument data must be list')

        self.counter = 0
        self.item_len = len(data)

    def call_coroutine(self, data):
        for item in data:
            self.counter += 1
            yield item

    def next(self):
        if self.coroutine is None:
            return None

        if self.counter < self.item_len:
            return next(self.coroutine)
        else:
            return None


class DataManager:

    def __init__(self, data, max_item=5):

        if type(data) is not list:
            raise ValueError('DataManager(data) -> data must be list')

        self.container = DataContainer(data)
        self.max_item = max_item

    def save_process_list(self, item_list):

        if len(item_list) < self.max_item:
            next_item = self.container.next()

            if next_item is not None:
                item_list.append(next_item)
                return code.OK, item_list
            else:
                return code.EMPTY, item_list
        return code.FULL, item_list

    def get_item_list(self):

        item_list = []
        res_code = code.OK

        for c in range(0, self.max_item):
            _code, item_list = self.save_process_list(item_list)
            res_code = _code

            if _code is code.EMPTY or _code is code.FULL:
                break
        return res_code, item_list

