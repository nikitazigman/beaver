def stable_marriage_problem(man_p, girl_p):
    mans_indexes = [0 for _ in range(len(man_p))]
    pairs = {}
    available_mans = list(range(len(man_p)))
    while len(available_mans) != 0:
        available_man = available_mans[-1]
        preferred_girl = man_p[available_man][mans_indexes[available_man]]
        if preferred_girl not in pairs:
            available_mans.pop()
            pairs[preferred_girl] = available_man
        else:
            current_man = pairs[preferred_girl]
            if girl_p[preferred_girl].index(current_man) > girl_p[preferred_girl].index(available_man):
                pairs[preferred_girl] = available_man
                available_mans.pop()
                available_mans.append(current_man)
        mans_indexes[available_man] += 1
    return pairs
