
BUFSIZ = 100

Query_type = ["ADD", "REMOVE", "UPDATE", "LAST_QUERY_TYPE"]

class query:
    def __init__(self):
        self.type = None
        self.data_index = 0

class query_provider:
    def __init__(self, path=None, fd=None, buffer=100, current=0, nb_query=0):
        self.path= path
        self.fd = fd
        self.buffer = [None]*buffer
        self.current = current
        self.nb_query = nb_query

    def initialise_query_provider(self, path) -> None:
        self.fd = open(path, "r")
        self.current = 0
        self.nb_query = 0

    def free_query_provider(self) -> None:
        self.fd.close()

    def get_next_query_set(self, next_query, sets) -> bool:

        if self.current >= self.nb_query:
            self.current = 0
            
            line = self.fd.readline()
            line = line[:-1]

            if line != '':
                self.nb_query = int(line)
            else:
                return False

        next_query.data_index = self.nb_query
        next_query.type = "REMOVE" if sets.has_element_set_collection(next_query.data_index) else "ADD"

        self.current += 1
        return True

    def get_next_query_lookup(self, next_query, lookup) -> int:
        if self.current >= self.nb_query:
            self.current= 0
            self.nb_query = self.fd.readline()
            if not self.nb_query:
                return 0

        next_query.data_index = self.buffer[self.current]
        if lookup.has_element_lookup(next_query.data_index):
            next_query.type = "REMOVE"
        else:
            next_query.type = "ADD"
        self.current +=1
        return 1

    def get_next_query_trajectories(self, next_query) -> int:
        if self.current >= self.nb_query:
            self.current= 0
            self.nb_query = self.fd.readline()
            if not self.nb_query:
                return 0

        next_query.data_index= self.buffer[self.current]
        next_query.type = "ADD"
        self.current += 1
        return 1
