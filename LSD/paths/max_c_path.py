from LSD.cycles import cycle_distance
from LSD.colors import BLACK, RED
from LSD.paths.dp import finish_subtree
from math import inf


def caculate_cmax(g, cycle, postorder, inorder, i):
    k = len(cycle)
    
    def cycle_min(*args):
        min_value = inf
        min_position = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value < min_value:
                min_value = new_value
                min_position = x
        return min_position
    
    def cycle_max(*args):
        max_value = -1
        max_position = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value > max_value:
                max_value = new_value
                max_position = x
        return max_position
    
    def checkbackedge(w, u):
        return postorder.index(w) < postorder.index(u)
    
    for j in range(len(postorder)):
        v = postorder[j]
        inpos = inorder.index(v)
        g.property(v, "link", inpos)
        for child in g.successors(v):
            color = g.get_color(child)
            # Is in cycle
            if child in cycle:
                pos = cycle.index(child)
                g.update_property(v, "min", cycle_min, pos)
                g.update_property(v, "max", cycle_max, pos)
            # Do nothing when in other run complete finished
            elif color != BLACK:
                # Is back edge
                if color != RED and checkbackedge(v, child):
                    g.update_property(v, "link", min, inorder.index(child))
                # Is no back edge
                else:
                    # look for one vertex cover
                    if g.property(child, "min") is not None and \
                            cycle_distance(k, i, g.property(child, "min")) > cycle_distance(k, i,
                                                                                            g.property(child, "max")):
                        return True, g.property(child, "min")
                    # Update values
                    g.update_property(v, "min", cycle_min, g.property(child, "min"))
                    g.update_property(v, "max", cycle_max, g.property(child, "max"))
                    # If not finished
                    if color != RED:
                        g.update_property(v, "link", min, g.property(child, "link"))
        # Finished subtree
        if g.property(v, "link") == inpos:
            finish_subtree(g, v)
    return False, g.property(cycle[i], "max")
