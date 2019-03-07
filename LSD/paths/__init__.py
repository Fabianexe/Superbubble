from LSD.dfs_tree import create_tree
from LSD.paths.max_c_path import caculate_cmax

def find_paths(g, cycle):
    ret = []
    for i in range(len(cycle)):
        c = cycle[i]
        postorder, inorder = create_tree(g, c, cycle)
        cover, value = caculate_cmax(g, cycle, postorder, inorder, i)
        if cover:
            return True, value
        ret.append(value)
    return False, ret
