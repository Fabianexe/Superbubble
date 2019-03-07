from LSD.RMQ import RangeQuery
from LSD.detecter.outvalues import out_child2, out_parent2


def super_bubble_brankovice(c, toposort, reporter):
    """Find all superbubbles in a DAG after Brankovice at all."""
    ord_id = toposort.index
    
    def report(s, t):
        reporter.rep(toposort[ord_id(s): ord_id(t) + 1])
    
    out_parent_list = []
    out_child_list = []
    for k in range(len(toposort)):
        out_child_list.append(out_child2(toposort[k], c, toposort))
        out_parent_list.append(out_parent2(toposort[k], c, toposort))
    out_child_rmq = RangeQuery(out_child_list, max)
    out_parent_rmq = RangeQuery(out_parent_list, min)
    prev_ent = None
    alternative_entrance = {}
    previous_entrance = []
    candidates = []
    backcand = {}
    for k in range(len(toposort)):
        previous_entrance.append(prev_ent)
        v = toposort[k]
        alternative_entrance[v] = None
        if is_exit(k, c, toposort):
            insert_exit(v, candidates)
        if is_entrance(k, c, toposort):
            insert_entrance(v, candidates, backcand)
            prev_ent = v
    while len(candidates) != 0:
        if candidates[-1][1]:
            delete_tail(candidates)
        else:
            report_super_bubble(candidates[0][0], candidates[-1][0], c, candidates, backcand, toposort, ord_id,
                                previous_entrance,
                                alternative_entrance, out_child_rmq, out_parent_rmq, report)


def report_super_bubble(start_vertex, exit_vertex, c, candidates, backcand, toposort, ord_id, previous_entrance,
                        alternative_entrance, out_child_rmq, out_parent_rmq, report):
    """Recusive call to find a superbubble"""
    if (start_vertex is None) or (exit_vertex is None) or (ord_id(start_vertex) >= ord_id(exit_vertex)):
        delete_tail(candidates)
        return
    s = previous_entrance[ord_id(exit_vertex)]
    valid = None
    while s is not None and ord_id(s) >= ord_id(start_vertex):
        valid = validate_super_bubble(s, exit_vertex, c, toposort, ord_id, out_child_rmq, out_parent_rmq,
                                      previous_entrance)
        if (valid == s) or (valid == alternative_entrance[s]) or valid == -1:
            break
        alternative_entrance[s] = valid
        s = valid
    delete_tail(candidates)
    if s is not None and valid == s:
        report(s, exit_vertex)
        while candidates[-1][0] != s:
            if candidates[-1][1]:
                delete_tail(candidates)
            else:
                report_super_bubble(next_candidate(s, candidates, backcand), candidates[-1][0], c, candidates, backcand,
                                    toposort, ord_id, previous_entrance, alternative_entrance, out_child_rmq,
                                    out_parent_rmq, report)


def validate_super_bubble(start_vertex, end_vertex, c, toposort, ord_id, out_child_rmq, out_parent_rmq,
                          previous_entrance):
    """Validate a superbubble"""
    start = ord_id(start_vertex)
    end = ord_id(end_vertex)
    # end is exclusive
    outchild = out_child_rmq.query(start, end)
    # end is exclusive
    outparent = out_parent_rmq.query(start + 1, end + 1)
    if outchild != end or outparent == -1:
        return -1
    if outparent == start:
        return start_vertex
    elif is_entrance(outparent, c, toposort):
        return toposort[outparent]
    else:
        return previous_entrance[outparent]


def is_exit(pos, c, toposort):
    """Check if a vertex is a exit"""
    if pos == 0:
        return False
    return pos == out_child2(toposort[pos - 1], c, toposort)


def is_entrance(pos, c, toposort):
    """Check if a vertex is a entrance"""
    if pos + 1 == len(toposort):
        return False
    return pos == out_parent2(toposort[pos + 1], c, toposort)


def insert_exit(v, candidates):
    """Insert a exit in the candidates list"""
    candidates.append((v, False))


def insert_entrance(v, candidates, backcand):
    """Insert a entrance in the candidates list"""
    backcand[v] = len(candidates)
    candidates.append((v, True))


def delete_tail(candidates):
    """Delete the tail of the candidate list"""
    del candidates[-1]


def next_candidate(v, candidates, backcand):
    """Get the next candidate to a entrance"""
    return candidates[backcand[v] + 1]
