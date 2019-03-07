from LSD.inout import load

if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    g = load(path)
    vertices = set()
    for v in g:
        if g.in_degree(v) == 0:
            stack = [v]
            while stack:
                n = stack.pop()
                if n not in vertices:
                    vertices.add(n)
                    stack += list(g.succ[n])
    
    print(len(list(vertices)))
            
        
    