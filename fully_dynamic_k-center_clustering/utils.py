import math
import random

class Log:
    def __init__(self, path, long_log=0):
        self.log_file=path
        self.long_log=long_log

    def log_ceil(self, n, base) -> float:
        return float(math.ceil(math.log(n) / math.log(base)))

    def shuffle_array(self, array, size) -> None:
        if size:
            for i in range(0, size-1):
                pick = i + random.randint(0,2147483647) % (size - i)
                array[i],array[pick] = array[pick], array[i]

    def enable_log(self, path) -> None:
        if path:
            log_file = open(path, "w")
            long_log = 0

    def enable_long_log(self, path) -> None:
        log_file = open(path, "w")
        long_log = 1

    def disable_log(self):
        if log_file:
            log_file.close()

    def get_log_file(self):
        return log_file

    def has_log(self):
        return log_file != None

    def has_long_log(self):
        return 0 != long_log

log = Log("test.log", 0)
#from utils import log
