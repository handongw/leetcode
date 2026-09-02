from typing import List
DEBUG = False

class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        m = len(matrix)
        n = len(matrix[0])

        column_height = [ 0 for _ in range(n)] # store rectangle height at each row
        largest_rectangle_area = 0  # partial result

        for r in range(m):
            # updated_height = [ 0 for _ in range(n)]
            if DEBUG:
                print(f"\n    r={r} row={matrix[r]}")
            # scan row r and update column_height
            for c in range(n):
                if matrix[r][c] == '0':
                    column_height[c] = 0
                else: # matrix[r][c] is '1':
                    column_height[c] = 1 + column_height[c]
            if DEBUG:
                print(f"    r={r} column_height={column_height}")
            # find all rectangles based on heights
            height_count_array = [[0,0] for _ in range(n)] # [[height, count]]
            height_count_size = 0

            for i in range(n):
                height = column_height[i]

                if height == 0:
                    height_count_size = 0 # clear height_count_array
                else:
                    # find last k where where height_count_array[k][0] <= height
                    lo = 0 
                    hi = height_count_size - 1
                    last_idx = -1

                    while lo <= hi:
                        mid = (lo+hi) // 2
                        if DEBUG:
                            print(f"    mid {mid} = ({lo}+{hi}) // 2 height={height}")
                        if height_count_array[mid][0] <= height:
                            last_idx = max(last_idx, mid)
                            lo = mid + 1
                        else:
                            hi = mid - 1
                    if DEBUG:        
                        print(f"    last_idx={last_idx}")

                    if last_idx == -1: # no such k exist
                        extra_height_count = height_count_array[0][1] if height_count_size > 0 else 0

                        height_count_array[0][0] = height
                        height_count_array[0][1] = (1+extra_height_count)
                        height_count_size = 1
                    else:
                        extra_height_count = height_count_array[last_idx+1][1] if last_idx+1 < height_count_size else 0

                        height_count_size = last_idx+1
                        for k in range(height_count_size):
                            height_count_array[k][1] += 1
                            if DEBUG:
                                assert height_count_array[k][0] <= height, f"assert height_count_array[{k}][0] <= {height}"

                        if height_count_array[last_idx][0] == height:
                            # height_count_array[last_idx][1] += extra_height_count
                            pass
                        else:
                            # append a new [height, count]
                            height_count_array[height_count_size][0] = height
                            height_count_array[height_count_size][1] = (1+extra_height_count)
                            height_count_size += 1
                    if DEBUG:
                        print(f"    height_count_array={height_count_array[0:height_count_size]} ")        
                    for k in range(height_count_size):
                        largest_rectangle_area = max(largest_rectangle_area, height_count_array[k][0] * height_count_array[k][1])


        return largest_rectangle_area
