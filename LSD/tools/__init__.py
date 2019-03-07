
def get_superbubble(s, t, g):
    print("Get vertices of superbubble: {s}-{t} ".format(s=s, t=t))
    vertices = set()
    vertices.add(s)
    stack = [(iter(list(g.successors(s))),s)]
    visited = set()
    while stack:
        children = stack[-1]
        try:
            child = next(children[0])
            if check_pre(child, g, visited) and children[1] != t:
                visited.add(child)
                stack.append([iter(list(g.successors(child))),child])
        except StopIteration:
            last = stack.pop()[1]
            for v in g.successors(last):
                vertices.add(v)
            for v in g.predecessors(last):
                vertices.add(v)
    return g.subgraph(vertices)

def check_pre(v, g, visited):
    for v2 in g.predecessors(v):
        if v2 not in visited:
            return False
    return True

def draw_graph(g, path="test.png"):
    print("Drae Graph")
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import networkx as nx
    plt.clf()
    nx.draw(g, with_labels=True)
    plt.savefig(path)