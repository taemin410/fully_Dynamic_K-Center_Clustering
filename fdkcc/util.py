import math
import random

def log_ceil(n, base) -> float:
    return float(math.ceil(math.log(n) / math.log(base)))

def shuffle_array(array, size) -> None:
    if size:
        for i in range(0, size-1):
            pick = i + random.randint(0,2147483647) % (size - i)
            array[i],array[pick] = array[pick], array[i]

class Log:

    def __init__(self, path, long_log=0):
        # self.log_file=path
        self.long_log=long_log
        self.enable_log(path)

    def log_ceil(self, n, base) -> float:
        return float(math.ceil(math.log(n) / math.log(base)))


    def enable_log(self, path) -> None:
        if path:
            self.log_file = open(path, "w")
            self.long_log = 0

    def enable_long_log(self, path) -> None:
        self.log_file = open(path, "w")
        self.long_log = 1

    def disable_log(self):
        if self.log_file:
            self.log_file.close()

    def get_log_file(self):
        return self.log_file

    def has_log(self):
        return self.log_file != None

    def has_long_log(self):
        return 0 != self.long_log

log_ = Log("cluster_information.log", 0)

