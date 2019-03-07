
def onodera(g, reporter):
    for s in g:
        dag = onodera_detect(s, g)
        if dag:
            reporter.rep(dag)


def onodera_detect(s, g):
    dag = []
    nextset = set()
    visited = set()
    seen = set()
    nextset.add(s)
    seen.add(s)
    while len(nextset):
        v = nextset.pop()
        seen.remove(v)
        visited.add(v)
        dag.append(v)
        if not g.out_degree(v):
            return
        for u in g.successors(v):
            if u == s:
                return
            seen.add(u)
            if parentsvisited(u, g, visited):
                nextset.add(u)
        if len(nextset) == 1 and len(seen) == 1:
            t = nextset.pop()
            dag.append(t)
            return dag


def parentsvisited(u, g, visited):
    for w in g.predecessors(u):
        if w not in visited:
            return False
    return True
