from fdkcc.util import log_ceil, shuffle_array, log_, Log
import random
import pytest 

@pytest.fixture
def create_log_object(tmpdir):
    
    logfiledir = tmpdir.join("logfile.txt")

    return Log(logfiledir), logfiledir


def test_Log_class(create_log_object):

    LOG, logfiledir = create_log_object

    LOG_ = LOG.get_log_file()
    LOG_.write("TEST LOG FILE WRITE")
    LOG.disable_log() #close the log file 

    f = open(logfiledir) #open file
    assert f.readline() == "TEST LOG FILE WRITE"
    f.close()


def test_log_ceil():
    #ceiling for 1000 in base 2 is 1024 which is 2^10 
    base = 2
    N = 1000
    ceiling = 10 

    assert log_ceil(N,base) == ceiling


def test_shuffle_array():
    SIZE=10
    LIST_TO_BE_SHUFFLED = random.sample(range(-180, 180), SIZE)
    LIST_TO_BE_COMPARED = LIST_TO_BE_SHUFFLED.copy()

    shuffle_array(LIST_TO_BE_SHUFFLED, SIZE)

    assert LIST_TO_BE_COMPARED != LIST_TO_BE_SHUFFLED
    for i in LIST_TO_BE_COMPARED:
        assert i in LIST_TO_BE_SHUFFLED
    


