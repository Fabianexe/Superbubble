"""The package to detect superbubbles in a DAG"""
from LSD.detecter.outvalues import out_child2, out_parent2


def dag_superbubble(g, order, reporter):
    """Detect all superbubbles in a DAG."""
    
    def report(i, o):
        reporter.rep(order[i: o + 1])
    
    # Either None is first elemant on stack or t is None!
    stack = []
    out_parent_map = []
    
    def f(pos):
        return len(order)-pos-1
    t = None
    for k in range(len(order)-1, -1, -1):
        v = order[k]
        child = out_child2(v, g, order)
        if child == k + 1:
            stack.append(t)
            t = k + 1
        else:
            while t is not None and t < child:
                t2 = stack.pop()
                if t2 is not None:
                    out_parent_map[f(t2)] = min(out_parent_map[f(t)], out_parent_map[f(t2)])
                t = t2
        if t is not None and out_parent_map[f(t)] == k:
            report(k, t)
            t2 = stack.pop()
            if t2 is not None:
                out_parent_map[f(t2)] = min(out_parent_map[f(t)], out_parent_map[f(t2)])
            t = t2
        out_parent_map.append(out_parent2(v, g, order))
        if t is not None:
            out_parent_map[f(t)] = min(out_parent_map[f(t)], out_parent_map[f(k)])
