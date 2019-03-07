"""The package that constructs the dags out of the subgraphs. This could be a sung graph or a simple DAG"""
from LSD.colors import GREY, BLACK


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
