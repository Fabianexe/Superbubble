from math import inf


class Order:
    """A order representation.
    Get a vertex on an arbitrary position in O(1).
    Get the position of an arbitrary vertex in O(1)."""
    
    def __init__(self, source=None, sink=None):
        """Init the order set source position -1 and sink and None position to infinity """
        self.order = []
        self.revers_order = {None: inf}
        if source is not None:
            self.revers_order[source] = -1
        if sink is not None:
            self.revers_order[sink] = inf
        self.pos = 0
    
    def add(self, v):
        """Add an element to the end of the order"""
        self.order.append(v)
        self.revers_order[v] = self.pos
        self.pos += 1
    
    def __len__(self):
        return len(self.order)
    
    def revers(self):
        self.order = list(reversed(self.order))
        for i in range(len(self.order)):
            self.revers_order[self.order[i]] = i
    
    @property
    def n(self):
        """Get the length of the order."""
        return len(self)
    
    def __getitem__(self, item):
        """Get element at position item"""
        return self.order[item]
    
    def get_position(self, v):
        """Get position of element v. If v not contained return -2"""
        try:
            return self.revers_order[v]
        except KeyError:
            return -2
    
    def __contains__(self, item):
        return item in self.revers_order
    
    def __str__(self):
        return str(self.order)