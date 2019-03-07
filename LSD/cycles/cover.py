from LSD.cycles import cycle_distance, generate_cycle_range


def find_cover_cut(cmax):
    k = len(cmax)
    # Calculate maximal global C-Path
    m = max((cycle_distance(k, i, cmax[i]), i) for i in range(k))[1]
    md = cycle_distance(k, m, cmax[m])
    laststart = m
    lastend = m
    # While laststart end not in maximal global C-Path
    while md <= cycle_distance(k, m, cmax[laststart]):
        # Calc maximal overtower
        next_path = None
        max_dist = 0
        for i in generate_cycle_range(k, lastend, cmax[laststart]):
            # Filter included paths
            if cycle_distance(k, i, cmax[i]) <= cycle_distance(k, i, cmax[laststart]):
                continue
            # Calc overtower and save max
            if cycle_distance(k, cmax[laststart], cmax[i]) > max_dist:
                max_dist = cycle_distance(k, cmax[laststart], cmax[i])
                next_path = i
        # If nothing overtower
        if next_path is None:
            # Return cut point
            return True, cmax[laststart]
        # Set next path to check
        lastend = cmax[laststart]
        laststart = next_path
    # Return Cycle cover
    return False, cmax[laststart]
