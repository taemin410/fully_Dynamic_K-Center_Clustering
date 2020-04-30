
class Center_comparator():
    def __init__(self, Ucenters, Vcenters):
        self.Ucenters = Ucenters #sets of centers before query
        self.Vcenters = Vcenters #sets of centers after query

    def get_set_difference(self):
        return self.Ucenters.difference(self.Vcenters)

    def get_difference_count(self):
        return len(self.Ucenters.difference(self.Vcenters))

    