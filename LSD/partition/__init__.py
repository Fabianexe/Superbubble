from networkx import strongly_connected_components


def get_strongly_connected_component(g):
    """Create the SCC components."""
    sccs = strongly_connected_components(g)
    dag = AuxiliaryGraph(0)
    n = 1
    non_singelton = []
    for scc in sccs:
        if len(scc) > 1 or next(iter(scc)) in set(g.successors(next(iter(scc)))):
            nsscc = AuxiliaryGraph(n)
            n += 1
            for v in scc:
                nsscc.add(v)
            non_singelton.append(nsscc)
        else:
            dag.add(next(iter(scc)))
    return dag, non_singelton


def create_auxiliary_graph(c, g):
    """Create the auxiliary graph that have the same superbubbles than g.
    This function also connects every source to a and every sink to b.
    This have the effect that every graph have exactly one source (a) and one sink (b).
    So that the computation of outChild and outParent are much easier."""
    c.copy_graph(g)
    
    for v in c:
        if g.in_degree(v) > c.in_degree(v) or c.in_degree(v) == 0:
            c.connect2source(v)
        if g.out_degree(v) > c.out_degree(v)or c.out_degree(v) == 0:
            c.connect2sink(v)


class AuxiliaryGraph:
    """The auxiliary graph representation."""

    
    def __init__(self, number):
        """Save the number of the graph."""
        self.vertices = set()
        self.number = number
        self.artificial_sink = "artificial_sink_{num}".format(num=self.number)
        self.artificial_source = "artificial_source_{num}".format(num=self.number)
        self.g = None
    
    def add(self, v):
        """Add a vertex to the axiliary graph."""
        self.vertices.add(v)
    
    def copy_graph(self, g):
        """Create with the vertices a induced subgraph. Add also a and b."""
        self.g = g.subgraph(self.vertices).copy()
        self.g.add_node(self.artificial_sink)
        self.g.add_node(self.artificial_source)
    
    def connect2sink(self, v):
        """Connect v with a"""
        self.g.add_edge(v, self.artificial_sink)
    
    def connect2source(self, v):
        """Connect v with b"""
        self.g.add_edge(self.artificial_source, v)
    
    def in_degree(self, v):
        """Get the in degree of a vertex."""
        return self.g.in_degree(v)
    
    def out_degree(self, v):
        """Get the out degree of a vertex"""
        return self.g.out_degree(v)
    
    def source_connected(self):
        """Check if a us connected."""
        return self.g.out_degree(self.artificial_source) != 0
    
    def sink_connected(self):
        """Check if b is connected."""
        return self.g.in_degree(self.artificial_sink) != 0
    
    def remove_edge(self, f, t):
        """Remove an edge from f to t from the graph."""
        self.g.remove_edge(f, t)
    
    def successors(self, v):
        """Get all successors of a vertex."""
        return list(self.g.successors(v))
    
    def predecessors(self, v):
        """Get all predeccessors of a vertex."""
        return list(self.g.predecessors(v))
    
    @property
    def nodes(self):
        """Get all vertices of a graph (including a and b)."""
        return self.g.nodes
    
    def set_color(self, v, c):
        """Set the color of v to c."""
        self.g.node[v]['c'] = c
    
    def get_color(self, v):
        """Get the color of v."""
        return self.g.node[v]['c']
    
    def has_no_color(self, v):
        """Check if a vertex have no color."""
        return 'c' not in self.g.node[v]
    
    def __iter__(self):
        """Iterate over the vertices of the graph (exluding a and b)."""
        return self.vertices.__iter__()