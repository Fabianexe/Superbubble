def choose_root(c):
    """Choose a or a b'' as root. The root is connected with a"""
    if c.source_connected():
        pass
    else:
        for predecessor in c.predecessors(c.b):
            for successor in c.successors(predecessor):
                if successor != c.b:
                    c.connect2source(successor)


def choose_random_root(c):
    """Choose a arbitrary root.
    To be deterministic the minimum vertex identifier is used"""
    r = next(iter(c))
    c.connect2source(r)
