from LSD.hashed_list import HashedList
from LSD.colors import GREY, BLACK


def create_dfs_order_cycle(v, g):
    order = HashedList()
    stack = [v]
    cycle = True
    v2 = None
    while stack:
        u = stack[-1]
        c = g.get_color(u)
        if c != GREY and c != BLACK:
            g.set_color(u, GREY)
            for w in g.successors(u):
                if cycle and w == v:
                    v2 = "{v}_split_duplicate".format(v=v)
                    order.append(v2)
                    cycle = False
                color = g.get_color(w)
                if color != GREY and color != BLACK:
                    stack.append(w)
        else:
            stack.pop()
            if c == GREY:
                order.append(u)
                g.set_color(u, BLACK)
    return order, v2


def create_dfs_order(v, g):
    order = HashedList()
    stack = [v]
    while stack:
        u = stack[-1]
        c = g.get_color(u)
        if c != GREY and c != BLACK:
            g.set_color(u, GREY)
            for w in g.successors(u):
                color = g.get_color(w)
                if color != GREY and color != BLACK:
                    stack.append(w)
        else:
            stack.pop()
            if c == GREY:
                order.append(u)
                g.set_color(u, BLACK)
    return order
