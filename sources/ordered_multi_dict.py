class OrderedMultiDict:
    def __init__(self, *args):
        self.container = []
        for key, value in args:
            self.add(key, value)

    def clear(self):
        self.container = []

    def copy(self):
        d = OrderedMultiDict()
        for item in self.items():
            d.add(item[0], item[1])
        return d

    def items(self):
        return iter(self.container)

    def keys(self):
        return map(lambda p: p[0], self.items())

    def values(self):
        return map(lambda p: p[1], self.items())

    def values_of(self, key):
        return list(map(
            lambda p: p[1],
            filter(lambda p: p[0] == key, self.container)
        ))

    def value_of(self, key):
        return self.values_of(key)[0]

    def __len__(self):
        return len(self.container)

    def __iter__(self):
        return self.keys()

    def __eq__(self, other):
        return self.container == other.container

    def add(self, key, value):
        self.container.append([key, value])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.container)

    def erase(self, key):
        self.container = list(filter(lambda p: p[0] != key, self.container))
