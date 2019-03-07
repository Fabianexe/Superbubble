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


