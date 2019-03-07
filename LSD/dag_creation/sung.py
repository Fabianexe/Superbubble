from LSD.colors import GREY, BLACK


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
            if child == c.b:
                c.g.add_edge("{v}_2".format(v=parent), c.b)
                c.g.remove_edge(parent, child)
            elif c.has_no_color(child):
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
