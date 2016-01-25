#! /usr/bin/env python
#coding: utf-8

import timeit

def break_rings(connections):
    from collections import Counter
    import itertools
    remain_rings = lambda L: set(itertools.chain(*L))
    remain_links = lambda r, L: [x for x in L if r not in x]
    rings = remain_rings(connections)
    count = 0
    while True:
        rings_after_break, links_after_break = len(rings), len(connections)
        next_break = None
        for r in rings:
            check = len(remain_rings(remain_links(r, connections)))
            # break the ring that reduces number of rings best
            if check < rings_after_break:
                rings_after_break = check
                next_break = r
            # if there are rings that reduce same number,
            # break the most connected ring
            elif check == rings_after_break:
                check = len(remain_links(r, connections))
                if check < links_after_break:
                    links_after_break = check
                    next_break = r
        connections = remain_links(next_break, connections)
        rings = remain_rings(connections)
        count += 1
        if len(rings) == 0:
            break
    return count

def break_rings_r1(rings):
    from itertools import combinations
    all_rings = set.union(*rings)
    for n in range(1, len(all_rings)):
        # it is NP-hard minimum vertex cover problem
        # can only be solved with brute force search
        for broken_rings in combinations(all_rings, n):
            remaining_rings = [pair.difference(broken_rings) for pair in rings]
            if all(len(rings) < 2 for rings in remaining_rings):
                return n

def break_rings_r2(connections):
    if len(connections) == 0:
        return 0
    r1, r2 = connections[0]
    return min(
            break_rings([c for c in connections if r1 not in c]) + 1,
            break_rings([c for c in connections if r2 not in c]) + 1)


def break_rings_r3(rings):
    from functools import reduce
    all_vertices = reduce(set.union, rings)
    adj = dict((v, reduce(set.union, (r for r in rings if v in r))) for v in all_vertices)

    def backtrack(size, vertices, x):
        """Bron-Kerbosch"""
        if not vertices and not x:
            yield size
        while vertices and not any(adj[i].isdisjoint(vertices) for i in x):
            v = vertices.pop()
            yield from backtrack(size + 1, vertices - adj[v], x - adj[v])
            x.add(v)

    return len(all_vertices) - max(backtrack(0, all_vertices, set()))

def main(function):

    s = """
from __main__ import %s

assert %s(({1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {4, 6})) == 3, "example"
assert %s(({1, 2}, {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4})) == 3, "All to all"
assert %s(({5, 6}, {4, 5}, {3, 4}, {3, 2}, {2, 1}, {1, 6})) == 3, "Chain"
assert %s(({8, 9}, {1, 9}, {1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {6, 7}, {8, 7})) == 5, "Long chain"
assert %s(({3,4},{5,6},{2,7},{1,5},{2,6},{8,4},{1,7},{4,5},{9,5},{2,3},{8,2},{2,4},{9,6},{5,7},{3,6},{1,3},)) == 5
assert %s(({1,2},{1,3},{1,5},{2,3},{2,4},{4,6},{5,6},)) == 3
    """%(function,function,function,function,function,function,function)

    print("%s\n\t%.6f s"%(function,timeit.timeit(s, number=100)))

if __name__ == '__main__':
    main("break_rings")
    main("break_rings_r1")
    main("break_rings_r2")
    main("break_rings_r3")

