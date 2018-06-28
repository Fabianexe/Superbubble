"""The package that constructs the dags out of the subgraphs. This could be a sung graph or a simple DAG"""

WHITE = 0
"""COLOR Definition"""
GREY = 1
"""COLOR Definition"""
BLACK = 2
"""COLOR Definition"""


def choose_root(c):
    """Choose a or a b'' as root. The root is connected with a"""
    if c.source_connected():
        pass
    else:
        for predecessor in c.predecessors(c.b):
            for successor in c.successors(predecessor):
                if successor != c.b:
                    c.connect2source(successor)


def construct_dag(c):
    """Construct the DAG that contain the same week superbubbles as G.
    In this procedure the DFS tree is constructed indirectly.
    It does a lineare version of a deep first search.
    The recusive version of the same algorithm would look like this::
    
        def construct_dag(c):
            recursive_dag(c, g.a)
            
    
        def recursive_dag(c, v):
            c.set_color(v, GREY)
            for child in c.successors(v):
                if c.has_no_color(child):
                    recursive_dag(g, child)
                elif c.get_color(child) == GREY:
                    c.remove_edge(v, child)
                    c.connect2sink(v)
                    c.connect2source(child)
            c.set_color(v, BLACK)
        
    """
    stack = [(c.a, iter(c.successors(c.a)))]
    while stack:
        parent, children = stack[-1]
        try:
            child = next(children)
            if c.has_no_color(child):
                c.set_color(child, GREY)
                stack.append((child, iter(c.successors(child))))
            elif c.get_color(child) == GREY:
                c.remove_edge(parent, child)
                c.connect2sink(parent)
                c.connect2source(child)
        except StopIteration:
            c.set_color(parent, BLACK)
            stack.pop()


def choose_random_root(c):
    """Choose a arbitrary root.
    To be deterministic the minimum vertex identifier is used"""
    r = min(c)
    c.connect2source(r)


def construct_sung_graph(c):
    """Construct the sung graph. That is also a DAG.
    In this procedure the DFS tree is constructed indirectly."""
    r = c.successors(c.a)[0]
    c.set_color(r, GREY)
    stack = [(r, iter(c.successors(r)))]
    while stack:
        parent, children = stack[-1]
        try:
            child = next(children)
            if c.has_no_color(child):
                c.set_color(child, GREY)
                stack.append((child, iter(c.successors(child))))
                c.g.add_edge("{v}_2".format(v=parent), "{v}_2".format(v=child))
            elif c.get_color(child) == GREY:
                c.g.remove_edge(parent, child)
                c.g.add_edge(parent, "{v}_2".format(v=child))
            else:
                c.g.add_edge("{v}_2".format(v=parent), "{v}_2".format(v=child))
        except StopIteration:
            c.set_color(parent, BLACK)
            stack.pop()
    for v in c:
        v2 = "{v}_2".format(v=v)
        if c.g.out_degree(v2) == 0:
            c.connect2sink(v2)
            break
