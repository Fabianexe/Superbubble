"""The package to detect superbubbles in a DAG"""
from math import inf as infinity


def out_child(v, g, order):
    """Calculate the outChild value of an vertex.
    Note that by construction every vertex beside b have a successor."""
    maximum = -1
    for v2 in g.successors(v):
        maximum = max(maximum, order.get_position(v2))
    return maximum


def out_parent(v, g, order):
    """Calculate the outParent value of an vertex.
        Note that by construction every vertex beside a have a predecessor."""
    minimum = infinity
    for v2 in g.predecessors(v):
        minimum = min(minimum, order.get_position(v2))
    return minimum


def dag_superbubble(g, order, reporter):
    """Detect all superbubbles in a DAG."""
    def report(i, o):
        reporter.rep(order[i: o + 1])
    
    stack = Stack()
    out_parent_map = {None: -3}
    t = None
    for k in range(order.n-1, -1, -1):
        v = order[k]
        child = out_child(v, g, order)
        if child == k+1:
            stack.put(t)
            t = order[k + 1]
        while order.get_position(t) < child:
            t2 = stack.pop()
            out_parent_map[t2] = min(out_parent_map[t], out_parent_map[t2])
            t = t2
        if out_parent_map[t] == k:
            report(k, order.get_position(t))
            t2 = stack.pop()
            out_parent_map[t2] = min(out_parent_map[t], out_parent_map[t2])
            t = t2
        out_parent_map[v] = out_parent(v, g, order)
        out_parent_map[t] = min(out_parent_map[t], out_parent_map[v])


class Stack:
    """A simple stack implementation that return None when the stack is empty."""
    def __init__(self):
        self.list = []
    
    def put(self, c):
        if c is not None:
            self.list.append(c)
    
    def pop(self):
        if len(self.list) == 0:
            return None
        return self.list.pop()

