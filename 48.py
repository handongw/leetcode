import copy
import traceback
from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """

        size = len(matrix)
        if size == 1:
            return None

        half_size = size // 2
        # is_odd = size & 0x1 != 0

        def rotate90(pos):
            # i, j = pos
            return (pos[1], size-1-pos[0])
            # if is_odd:
            #     return (j, size-1-i)
            # else:
            #     return (j, size-1-i)    

        # we need to rotate (size // 2) outer rims one by one

        for rim in range(half_size):
            # rim start at (rim, rim) and end at (size-1-rim, size-1-rim)
            for j in range(rim, size-1-rim):
                pos1 = (rim, j)
                pos2 = rotate90(pos1)
                pos3 = rotate90(pos2)
                pos4 = rotate90(pos3)

                # print(f"pos1={pos1} pos2={pos2} pos3={pos3} pos4={pos4}")

                tmp = matrix[pos1[0]][pos1[1]]
                matrix[pos1[0]][pos1[1]] = matrix[pos4[0]][pos4[1]]
                matrix[pos4[0]][pos4[1]] = matrix[pos3[0]][pos3[1]]
                matrix[pos3[0]][pos3[1]] = matrix[pos2[0]][pos2[1]]
                matrix[pos2[0]][pos2[1]] = tmp




if __name__ == "__main__":
    solver = Solution()

    test_cases = [
        {
            "matrix": [[1]],
            "expected": [[1]],
        },
        {
            "matrix": [[1, 2], [3, 4]],
            "expected": [[3, 1], [4, 2]],
        },
        {
            "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "expected": [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
        },
        {
            "matrix": [
                [5, 1, 9, 11],
                [2, 4, 8, 10],
                [13, 3, 6, 7],
                [15, 14, 12, 16],
            ],
            "expected": [
                [15, 13, 2, 5],
                [14, 3, 4, 1],
                [12, 6, 8, 9],
                [16, 7, 10, 11],
            ],
        },
        {
            "matrix": [[-1, 0], [0, -1]],
            "expected": [[0, -1], [-1, 0]],
        },
    ]

    # cases = [4]
    cases = None
    import time
    t1 = int(time.time() * 1000)
    succCount = 0
    totalCount = 0
    for idx, case in enumerate(test_cases, start=1):
        if cases is None or idx in cases:
            totalCount += 1
            matrix = copy.deepcopy(case["matrix"])
            expected = case["expected"]
            try:
                print(f"\n\nCase {idx}: {case['matrix']}\n")
                solver.rotate(matrix)
                actual = matrix
                print(f"Case {idx}:")
                print(f"  matrix={case['matrix']}")
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

