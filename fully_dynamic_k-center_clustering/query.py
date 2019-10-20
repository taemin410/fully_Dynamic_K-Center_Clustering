
BUFSIZ = 100

Query_type = ["ADD", "REMOVE", "UPDATE", "LAST_QUERY_TYPE"]

class query:
    def __init__(self, type, data_index):
        self.type = type
        self.data_index = data_index

class query_provider:
    def __init__(self):
        self.fd = None
        self.buffer = [0]*100
        self.current = 0
        self.nb_query = 0


    def initialise_query_provider(self, path) -> None:
        self.fd = open(path, "r")
        self.current = 0
        self.nb_query = 0


    def free_query_provider(self) -> None:
        self.fd.close()

    def get_next_query_set(self, next_query, sets) -> int:
        if self.current >= self.nb_query:
            self.current = 0
            self.nb_query = self.fd.readline()

            if not self.nb_query:
                return 0

        next_query.data_index = self.buffer[self.current]
        if sets.has_element_set_collection(next_query.data_index):
            next_query.type = "REMOVE"
        else:
            next_query.type = "ADD"
        self.current += 1
        return 1

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
