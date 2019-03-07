class HashedList:
    def __init__(self, iterable=None):
        self.list = []
        self.dict = {}
        if iterable is not None:
            for v in iterable:
                self.append(v)
    
    def append(self, v):
        self.dict[v] = len(self.list)
        self.list.append(v)
    
    def index(self, v):
        try:
            return self.dict[v]
        except KeyError:
            return -2
    
    def __len__(self):
        return len(self.list)
    
    def __getitem__(self, item):
        return self.list[item]
    
    def __iter__(self):
        return iter(self.list)
    
    def __contains__(self, item):
        return item in self.dict
    
    def __str__(self):
        return str(self.list)
    
    def add_pseudo_revers(self, key, value):
        self.dict[key] = value
