

Query_type = ["ADD", "REMOVE", "UPDATE", "LAST_QUERY_TYPE"]

class query:
    def __init__(self, type, data_index):
        self.type = type
        self.data_index = data_index

class query_provider:
    def __init(self, path, fd, buffer, current, nb_query):
        self.path = path
        self.fd = fd
        self.buffer = [0]*BUFSIZ
        self.current = current
        self.nb_query = nb_query


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
        next_query.type = sets.has_element_set_collection(next_query.data_index) ? "REMOVE" : "ADD"
        self.current += 1
        return 1

    def get_next_query_lookup(self, next_query, lookup) -> int:
        if self.current >= self.nb_query:
            self.current= 0
            self.nb_query = self.fd.readline()
            if not self.nb_query:
                return 0

        next_query.data_index = self.buffer[self.current]
        next_query.type = lookup.has_element_lookup(next_query.data_index) ? "REMOVE" : "ADD"
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
