from LSD.colors import WHITE, GREEN, YELLOW
from LSD.hashed_list import HashedList


def find_cycles(g):
    for v in g.nodes:
        if g.get_color(v) == WHITE:
            stack = [v]
            while stack:
                u = stack[-1]
                c = g.get_color(u)
                if c == WHITE:
                    g.set_color(u, GREEN)
                    for w in g.successors(u):
                        wc = g.get_color(w)
                        if wc == WHITE:
                            stack.append(w)
                        elif wc == GREEN:
                            cycle = []
                            while stack[-1] != w:
                                x = stack.pop()
                                if g.get_color(x) == GREEN:
                                    cycle.append(x)
                            cycle.append(stack.pop())
                            yield HashedList(reversed(cycle))
                            break
                else:
                    if c == GREEN:
                        g.set_color(u, YELLOW)
                    stack.pop()


def cycle_distance(k, i, end):
    if end > i:
        return end - i - 1
    return end + k - i - 1


def generate_cycle_range(k, pos, end):
    i = pos
    if end < pos:
        while i < end or i >= pos:
            yield i
            i = (i + 1) % k
    else:
        while i < end:
            yield i
            i += 1
