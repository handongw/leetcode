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
            height_stack = [[-1, -1]]  # item is [height, start_idx]
            for c in range(n):
                height = column_height[c]

                last_popup = None
                while height_stack[-1][0] > height:
                    last_popup = height_stack.pop()
                    area = last_popup[0] * (c - last_popup[1]) 
                    largest_rectangle_area = max(largest_rectangle_area, area)
                
                if height>0:
                    if height_stack[-1][0] == height:
                        pass
                    elif last_popup:
                        height_stack.append([height, last_popup[1]])
                    else:
                        height_stack.append([height, c])


            for last_popup in height_stack:
                area = last_popup[0] * (n - last_popup[1]) 
                largest_rectangle_area = max(largest_rectangle_area, area)


        return largest_rectangle_area
