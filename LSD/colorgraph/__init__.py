from LSD.colors import WHITE

class ColorGraph:
    """The auxiliary graph representation.
    It is in the core a subgraph of the complete NetworkX graph.
    However, it have an other initialisation, some extra features and depend slightly different."""
    
    def __init__(self, g):
        """Save the the graph."""
        self.g = g
        for v in self.nodes:
            self.set_color(v, WHITE)
    
    def in_degree(self, v):
        """Get the in degree of a vertex."""
        return self.g.in_degree(v)
    
    def out_degree(self, v):
        """Get the out degree of a vertex"""
        return self.g.out_degree(v)
    
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
    
    def property(self, v, key, value=None):
        if value is not None:
            self.g.node[v][key] = value
        else:
            try:
                return self.g.node[v][key]
            except KeyError:
                return None
    
    def update_property(self, v, key, func, *values):
        values = list(filter(lambda x: x is not None, values))
        if values:
            node = self.g.node[v]
            if key in node:
                node[key] = func(node[key], *values)
            else:
                if len(values) > 1:
                    node[key] = func(*values)
                else:
                    node[key] = values[0]
   
    def __iter__(self):
        """Iterate over the vertices of the graph (excluding a and b)."""
        return iter(self.nodes)
    
    def __str__(self):
        s = ", ".join("{v} {color}".format(v=v, color=self.get_color(v)) for v in self.nodes)
        s += "\n"
        s += ", ".join(str(s) for s in self.g.edges)
        s += "\n"
        return s
