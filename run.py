import sys
import time
import utils
from Manager.ScrapperManager import ScrapperManager

useage = 'python run.py artist_size start_artist_id'

if len(sys.argv) != 3:
    print(useage)
    # exit(1)#

args = sys.argv

if utils.is_number(args[1]) is not True \
    or utils.is_number(args[2]) is not True:
    print('arguments must me number')
    exit(2)

artist_size = args[1]   # 100
start_id = args[2]      # 771461

manager = ScrapperManager()
start_time = time.time()
manager.start(artist_size, start_id)
end_time = time.time()

print('{}'.format(end_time - start_time))
