from LSD.colors import WHITE
from LSD.cycles import find_cycles
from LSD.paths import find_paths
from LSD.cycles.cover import find_cover_cut

def generate_roots(g):
    for v in g.nodes:
        if g.get_color(v) == WHITE:
            if g.in_degree(v) == 0:
                yield v, False
    
    for cycle in find_cycles(g):
        cover, value = find_paths(g, cycle)
        if cover:
            yield cycle[value], False
        else:
            paths = value
            cutpoint, position = find_cover_cut(paths)
            if cutpoint:
                yield cycle[position], True
            else:
                yield cycle[position], False
