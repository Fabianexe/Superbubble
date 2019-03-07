from LSD.hashed_list import HashedList
from LSD.colors import ORANGE, BLACK, RED

def create_tree(g, c, cycle):
    postorder = HashedList()
    inorder = HashedList()
    #Add cycle vertex as first in preorder
    inorder.append(c)
    stack = [c]
    #Create tree
    while stack:
        top = stack[-1]
        color = g.get_color(top)
        if color != ORANGE:
            g.set_color(top, ORANGE)
            #New vertex found
            inorder.append(top)
            for child in g.successors(top):
                #No backedge or finished vertex or cycle vertex
                if g.get_color(child) not in [BLACK, ORANGE, RED] and child not in cycle:
                    stack.append(child)
        #Is already orange and so finished now
        else:
            #When not already finished
            if top not in postorder:
                #Add postorder
                postorder.append(top)
            #Remove from stack
            stack.pop()
    return postorder, inorder