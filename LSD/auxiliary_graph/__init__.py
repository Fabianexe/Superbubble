"""The package that contains the auxiliary graph class."""


class AuxiliaryGraph:
    """The auxiliary graph representation.
    It is in the core a subgraph of the complete NetworkX graph.
    However, it have an other initialisation, some extra features and depend slightly different."""
    
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
    
    def add_edge(self,v, v2):
        self.g.add_edge(v, v2)
    
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
        """Check if a is connected."""
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

    @property
    def a(self):
        """Get the artificial source of the graph."""
        return self.artificial_source

    @property
    def b(self):
        """Get the artificial sink of the graph."""
        return self.artificial_sink

    @property
    def nr(self):
        """Get the number of this part."""
        return self.number
    
    def set_color(self, v, c, add=""):
        """Set the color of v to c."""
        self.g.node[v]['c'+add] = c
    
    def get_color(self, v, add=""):
        """Get the color of v."""
        return self.g.node[v]['c'+add]
    
    def has_no_color(self, v, add=""):
        """Check if a vertex have no color."""
        return 'c'+add not in self.g.node[v]
    
    def __iter__(self):
        """Iterate over the vertices of the graph (exluding a and b)."""
        return self.vertices.__iter__()
    
    def __str__(self):
        s = ", ".join(self.nodes)
        s += "\n"
        s += ", ".join(str(s) for s in self.g.edges)
        s += "\n"
        return s


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