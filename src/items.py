class ItemContainer():
    def __init__(self):
        self.container = {}
        self.min_key = 0

    def append(self, item) -> int:
        """This function adds the item to the dictionary and returns the key."""
        # this way, no keys will double
        self.min_key += 1
        self.container[self.min_key] = item
        return self.min_key

    def __getitem__(self, key):
        return self.container[key]

    def __setitem__(self, key, value):
        self.container[key] = value