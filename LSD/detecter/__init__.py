from LSD.detecter.outvalues import out_child, out_parent


def superbubble(g, order, reporter, v, v2=None):
    """Detect all superbubbles in a DFS-tree."""
    
    def report(i, o):
        reporter.rep(order[o: i + 1][::-1])
    
    # Either None is first element on stack or t is None!
    stack = []
    out_parent_map = []
    t = None
    for k in range(len(order)):
        child = out_child(k, g, order, v, v2)
        if child == k - 1:
            stack.append(t)
            t = k - 1
        else:
            while t is not None and t > child:
                t2 = stack.pop()
                if t2 is not None:
                    out_parent_map[t2] = max(out_parent_map[t], out_parent_map[t2])
                t = t2
        if t is not None and out_parent_map[t] == k:
            report(k, t)
            t2 = stack.pop()
            if t2 is not None:
                out_parent_map[t2] = max(out_parent_map[t], out_parent_map[t2])
            t = t2
        out_parent_map.append(out_parent(k, g, order, v, v2))
        if t is not None:
            out_parent_map[t] = max(out_parent_map[t], out_parent_map[k])
