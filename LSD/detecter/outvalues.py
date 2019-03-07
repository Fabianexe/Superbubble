from math import inf as infinity


def out_child2(v, g, order):
    """Calculate the outChild value of an vertex.
    Note that by construction every vertex beside b have a successor."""
    maximum = -1
    for v2 in g.successors(v):
        maximum = max(maximum, order.index(v2))
    return maximum


def out_parent2(v, g, order):
    """Calculate the outParent value of an vertex.
        Note that by construction every vertex beside a have a predecessor."""
    minimum = infinity
    for v2 in g.predecessors(v):
        minimum = min(minimum, order.index(v2))
    return minimum


def out_parent(k, g, order, v, v2):
    u = order[k]
    if u == v2:
        u = v
    if g.in_degree(u) == 0:
        return infinity
    maximum = -1
    for w in g.predecessors(u):
        pos = order.index(w)
        if pos <= k:
            return infinity
        maximum = max(maximum, pos)
    return maximum


def out_child(k, g, order, v, v2):
    u = order[k]
    if u == v2:
        u = v
    if g.out_degree(u) == 0:
        return -2
    minimum = infinity
    for w in g.successors(u):
        if w == v and v2 is not None:
            pos = order.index(v2)
        else:
            pos = order.index(w)
        if pos >= k:
            return -2
        minimum = min(minimum, pos)
    return minimum
