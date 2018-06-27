import math


def check_pre(v, g, order):
    """Check if all predecessors have already been placed."""
    if order.get_position(v) > -2:
        return False
    for v2 in g.predecessors(v):
        if order.get_position(v2) == -2:
            return False
    return True


def toposort(g):
    """Do a topological ordering of the graph"""
    order = Order(g.artificial_source, g.artificial_sink)
    stack = [iter(g.successors(g.artificial_source))]
    while stack:
        children = stack[-1]
        try:
            child = next(children)
            if check_pre(child, g.g, order):
                order.add(child)
                stack.append(iter(g.successors(child)))
        except StopIteration:
            stack.pop()
    return order


class Order:
    """A order representation.
    Get a vertex on an arbitrary position in O(1).
    Get the position of an arbitrary vertex in O(1)."""
    def __init__(self, source, sink):
        self.order = []
        self.revers = {source: -1, sink: math.inf, None: math.inf}
        self.pos = 0
    
    def add(self, v):
        self.order.append(v)
        self.revers[v] = self.pos
        self.pos += 1
    
    def __len__(self):
        return len(self.order)
    
    def __getitem__(self, item):
        return self.order[item]
    
    def __iter__(self):
        return self.order.__iter__()
    
    def get_position(self, v):
        try:
            return self.revers[v]
        except KeyError:
            return -2
