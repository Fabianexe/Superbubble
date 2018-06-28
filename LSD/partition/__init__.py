from networkx import strongly_connected_components
from LSD.auxiliary_graph import AuxiliaryGraph


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
