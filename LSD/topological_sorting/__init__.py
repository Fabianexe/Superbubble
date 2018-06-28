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
    """Do a topological ordering of the graph.
    It does a lineare version of a deep first search.
    The recusive version of the same algorithm would look like this::
    
        def toposort(g):
            order = Order(g.a, g.b)
            rec_call(g.a, order, g, lambda v: check_pre(v, g, order))
            return order
    
            
        def rec_call(v, order, g, check_predecessor):
            for child in g.successors(v):
                if check_predecessor(child):
                    order.add(child)
                    rec_call(child, order, g, check_predecessor)
    
    """
    order = Order(g.a, g.b)
    stack = [iter(g.successors(g.a))]
    while stack:
        children = stack[-1]
        try:
            child = next(children)
            if check_pre(child, g, order):
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
        """Init the order set source position -1 and sink and None position to infinity """
        self.order = []
        self.revers = {source: -1, sink: math.inf, None: math.inf}
        self.pos = 0
    
    def add(self, v):
        """Add an element to the end of the order"""
        self.order.append(v)
        self.revers[v] = self.pos
        self.pos += 1

    @property
    def n(self):
        """Get the length of the order."""
        return len(self.order)
    
    def __getitem__(self, item):
        """Get element at position item"""
        return self.order[item]
    
    def get_position(self, v):
        """Get position of element v. If v not contained return -2"""
        try:
            return self.revers[v]
        except KeyError:
            return -2
