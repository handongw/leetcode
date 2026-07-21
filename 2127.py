from typing import List

DEBUG = False

class Solution:
    def maximumInvitations(self, favorite: List[int]) -> int:
        n = len(favorite)
        if n <= 0:
            return 0

        if DEBUG:
            print(f"edges: {[ (i, favorite[i]) for i in range(n)]}")

        visited = [0] * n

        node_depth = [0] * n  # used to calculate ring size
        ring_size = []

        node_info = [None] * n  # used to track pair-with-wings vertex
        pair_map = {}           # used to gather pair-with-wing size

        def update_pair_info(pair, small_end_size, large_end_size):
            rec = pair_map.setdefault(pair, {"small_end_size":1, "large_end_size":1})
            if DEBUG:
                print(f"    updare pair rec={rec} args: {(pair, small_end_size, large_end_size)}")

            if small_end_size:
                rec["small_end_size"] = max(rec["small_end_size"], small_end_size)
            else:
                rec["large_end_size"] = max(rec["large_end_size"], large_end_size)

        def dfs(v, depth):
            # v is part of long loop: length>=3
            # v is part of pair
            # v is part of path to a pair
            visited[v] = 1   
            node_depth[v] = depth         
            f = favorite[v]
            if DEBUG:
                print(f"dfs({v}) depth={depth} f={f} visited[f]={visited[f]}")

            if visited[f] == 0:
                ret = dfs(f, depth+1)
                if ret:
                    pair, small_end_size, large_end_size = ret
                    if not node_info[v]:
                        if small_end_size:
                            small_end_size += 1
                        else:
                            large_end_size += 1

                        node_info[v] = (pair, small_end_size, large_end_size)    
                visited[v] = 2    
                return node_info[v]    
            elif visited[f] == 1: # found cycle 
                # Functional graph optimization:
                # once a back-edge is found, the entire cycle is determined.
                # Mark cycle nodes as resolved immediately and unwind.
                visited[f] = 2
                visited[v] = 2    

                if favorite[f] == v: # found a cyclic pair (v, f)
                    if DEBUG:
                        print(f"    found pair {(v, f)}")
                    if v < f:
                        pair = (v, f)
                        node_info[v] = (pair, 1, None) # (pair, small_end_size, large_end_size)    
                        node_info[f] = (pair, None, 1)
                        if DEBUG:
                            print(f"            node_info={node_info}")
                    else:
                        pair = (f, v)
                        node_info[f] = (pair, 1, None)
                        node_info[v] = (pair, None, 1)
                        if DEBUG:
                            print(f"            node_info={node_info}")

                    return node_info[v]
                else: # found a long ring that has depth+1 vertex  
                    if DEBUG:
                        print(f"    found a ring: ")
                    ring_size.append(depth - node_depth[f]  +1)
                    return None
            else: 
                if DEBUG:
                    print(f"    reach DONE vertex {f}")
                if node_info[f]: # f reaches a pair-with-wings   
                    pair, small_end_size, large_end_size = node_info[f]
                    if small_end_size:
                            small_end_size += 1
                    else:
                        large_end_size += 1

                    node_info[v] = (pair, small_end_size, large_end_size)
                    if DEBUG:
                        print(f"            node_info={node_info}")
                visited[v] = 2        
                return node_info[v]

        for v in range(n):
            if visited[v] == 0:                
                ret = dfs(v, 0)    
                if ret:
                    update_pair_info(*ret)

        if DEBUG:
            print(f"ring_size={ring_size} pair_map={pair_map}")
            print(f"node_info={node_info}")

        ans1 = 0
        if ring_size:
            ans1 = max(ring_size)  # only one ring can be selected

        ans2 = 0    
        if pair_map:
            for x in pair_map.values():
                ans2 += x["small_end_size"]+x["large_end_size"]   # select all pair-with-wings
        return max(ans1, ans2)        
        
if __name__ == '__main__':
    import sys
    import time

    DEBUG = False
    selected_tests = None  # None: run all; else set of 1-based indices from argv

    for a in sys.argv[1:]:
        if a == "-d":
            DEBUG = True
        elif a.replace(",", "").isdigit() and "," in a:
            if selected_tests is None:
                selected_tests = set()
            for part in a.split(","):
                part = part.strip()
                if part.isdigit():
                    selected_tests.add(int(part))
        elif a.isdigit():
            if selected_tests is None:
                selected_tests = set()
            selected_tests.add(int(a))
        else:
            print(
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 4)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    # tests = [
    #     # 1. Single edge
    #     {
    #         "n": 1,  # test id
    #         "favorite":[2,2,1,2],
    #         "expected": 3,
    #     },
    # ]

    tests = [
    {
        "n": 1,  # smallest mutual pair
        "favorite": [1, 0],
        "expected": 2,
    },
    {
        "n": 2,  # simple 3-cycle
        "favorite": [1, 2, 0],
        "expected": 3,
    },
    {
        "n": 3,  # one chain into a mutual pair
        "favorite": [1, 0, 0],
        "expected": 3,
    },
    {
        "n": 4,  # chains on both sides of a mutual pair
        "favorite": [1, 0, 0, 1],
        "expected": 4,
    },
    {
        "n": 5,  # longer chain into one side only
        "favorite": [1, 0, 0, 2],
        "expected": 4,
    },
    {
        "n": 6,  # longer chains on both sides
        "favorite": [1, 0, 0, 2, 1, 4],
        "expected": 6,
    },
    {
        "n": 7,  # branching into one endpoint; only one branch can be used
        "favorite": [1, 0, 0, 0],
        "expected": 3,
    },
    {
        "n": 8,  # choose deepest branch only
        "favorite": [1, 0, 0, 2, 0, 4],
        "expected": 4,
    },
    {
        "n": 9,  # one 4-cycle, no attachments
        "favorite": [1, 2, 3, 0],
        "expected": 4,
    },
    {
        "n": 10,  # 4-cycle with incoming chains
        "favorite": [1, 2, 3, 0, 0, 4],
        "expected": 4,
    },
    {
        "n": 11,  # two disjoint mutual pairs
        "favorite": [1, 0, 3, 2],
        "expected": 4,
    },
    {
        "n": 12,  # multiple mutual pairs with wings
        "favorite": [1, 0, 0, 2, 5, 4],
        "expected": 6,
    },
    {
        "n": 13,  # large cycle beats pair-with-wings
        "favorite": [1, 2, 3, 4, 0, 6, 5],
        "expected": 5,
    },
    {
        "n": 14,  # pair-with-wings beats large cycle
        "favorite": [1, 0, 0, 2, 5, 4, 4],
        "expected": 7,
    },
    {
        "n": 15,  # several components, answer comes from one component only
        "favorite": [1, 2, 0, 4, 3],
        "expected": 3,
    },
    {
        "n": 16,  # official-style example
        "favorite": [2, 2, 1, 2],
        "expected": 3,
    },
    {
        "n": 17,  # star into a mutual pair
        "favorite": [1, 0, 0, 0, 0, 1],
        "expected": 4,
    },
    {
        "n": 18,  # deep chains into both sides
        "favorite": [1, 0, 0, 2, 1, 4, 5],
        "expected": 7,
    },
    {
        "n": 19,  # every node in one cycle
        "favorite": [1, 2, 3, 4, 5, 0],
        "expected": 6,
    },
    {
        "n": 20,  # mixed graph: cycle and pair-with-wings coexist
        "favorite": [1, 2, 0, 4, 3, 3, 5],
        "expected": 4,
    },
    {
        "n": 21,
        "favorite": [1,0,0,0,0],
        "expected": 3,   # many branches into one pair endpoint
    },
    {
        "n": 22,
        "favorite": [1,2,0,0,3],
        "expected": 3,   # attachments into ≥3 cycle ignored
    },
    {
        "n": 23,
        "favorite": [1,0,3,2,0,4,2,6],
        "expected": 8,   # multiple pairs, deep chains, summation
    },
    {
        "n": 24,
        "favorite": [1,0,3,2,0,4,2,6],
        "expected": 8,   # multiple pairs, deep chains, summation
    },
    {
        "n": 25,
        "favorite": [1,0,0,2,1,4,7,8,9,6,7,10,8],
        "expected": 6
    },
    {
        "n": 26,
        "favorite": [1,2,3,4,5,6,3,8,9,10,11,8],
        "expected": 4
    },
     {
        "n": 27,
        "favorite": [23,14,17,5,19,2,0,18,15,12,2,8,21,3,3,1,6,5,11,17,3,7,14,13],
        "expected": 3
    }
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        favorite = test["favorite"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} favorite={favorite[:20]}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.maximumInvitations(favorite)
            if result != expected:
                print(f"test {index} FAIL: n={test['n']}")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {index} OK: n={test['n']} (result={result})")
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
