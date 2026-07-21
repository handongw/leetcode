from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # Traverse edges and find max vertex value n
        n = 0
        for u, v in edges:
            n = max(n, u, v)
 
        # each vertex is its own leader iniitally
        leader_list = [ x for x in range(n+1)] 

        def find(v):
            if leader_list[v] == v:
                return v
            else:
                leader_list[v] = find(leader_list[v])
                return leader_list[v]


        for e in edges:
            v1, v2 = e
            # make v1 and v2 in the same group
            leader1 = find(v1)
            leader2 = find(v2)

            if(leader1 == leader2):
                return e
            else:
                leader_list[leader2] = leader1


        return None


if __name__ == "__main__":
    import traceback
    import time

    solver = Solution()

    test_cases = [
        {
            "edges": [[1, 2], [1, 3], [2, 3]],
            "expected": [2, 3],
        },
        {
            "edges": [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],
            "expected": [1, 4],
        },
        {
            "edges": [[1, 2], [1, 3], [2, 3], [3, 4]],
            "expected": [2, 3],
        },
    ]

    # cases = [1]
    cases = None
    t1 = int(time.time() * 1000)
    succCount = 0
    totalCount = 0
    for idx, case in enumerate(test_cases, start=1):
        if cases is None or idx in cases:
            totalCount += 1
            edges = case["edges"]
            expected = case["expected"]
            try:
                print(f"\n\nCase {idx}: edges={edges!r}\n")
                actual = solver.findRedundantConnection(edges)
                print(f"Case {idx}:")
                print(f"  edges   ={edges!r}")
                print(f"  expected={expected}")
                print(f"  actual  ={actual}")
                print(f"  Case {idx} pass    ={actual == expected}")
                print("\n")
                if actual == expected:
                    succCount += 1
            except Exception as exc:
                print(f"Case {idx} raised an exception: {exc}")
                traceback.print_exc()

    t2 = int(time.time() * 1000)
    print(f"   total time={t2-t1:,} ms  succ= {succCount}/{totalCount}")
