import time
from Manager.ScrapperManager import ScrapperManager

manager = ScrapperManager()
start_time = time.time()
manager.start(500, 771461)
end_time = time.time()

print('{}'.format(end_time - start_time))