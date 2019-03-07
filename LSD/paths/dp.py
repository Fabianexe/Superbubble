from LSD.colors import RED, ORANGE


def finish_subtree(g, v):
    minval = g.property(v, "min")
    maxval = g.property(v, "max")
    nexts = [v]
    g.set_color(v, RED)
    while nexts:
        u = nexts.pop()
        g.property(u, "min", minval)
        g.property(u, "max", maxval)
        for w in g.successors(u):
            if g.get_color(w) == ORANGE:
                g.set_color(w, RED)
                nexts.append(w)
