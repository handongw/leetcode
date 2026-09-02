class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        m = len(matrix)
        n = len(matrix[0])

        # how far a cell (r, c) can stretch right-ward with continuous 1 cells
        stretch_right_col = [ [ -1 for _ in range(n)] for _ in range(m)] # -1 mean can not stretch to right

        for r in range(m):
            right_1_col = -1
            prev_cell = 0
            for c in reversed(range(n)):
                if prev_cell == 0:
                    if matrix[r][c] == '0':
                        pass
                    else: # cell 0 to cell 1
                        right_1_col = c
                        stretch_right_col[r][c] = right_1_col
                        # print(f"    stretch_right_col[{r}][{c}] = {right_1_col}")
                        prev_cell = 1    
                else:
                    if matrix[r][c] == '0': # cell 1 to cell 0
                        right_1_col = -1
                        prev_cell = 0
                    else: # cell 1 to cell 1
                        stretch_right_col[r][c] = right_1_col
                        # print(f"    stretch_right_col[{r}][{c}] = {right_1_col}")

        # for r in range(m):
        #     print(f"{stretch_right_col[r]}") 

        # assume upper_left_cell is '1'
        def largest_rectangle(upper_left_cell):
            partial_result = 0
            r, c = upper_left_cell
            right_col = stretch_right_col[r][c]
            
            while r<m and matrix[r][c] == '1':
               right_col = min(stretch_right_col[r][c], right_col)
               rectangle_area = (r-upper_left_cell[0]+1) * (right_col-c+1)
               partial_result = max(rectangle_area, partial_result)
               r += 1
            return partial_result   

        result = 0
        for r in range(m):
            for c in range(n):
                if matrix[r][c] == '1':
                    area = largest_rectangle((r, c))
                    result = max(result, area)
                    # print(f"    largest_rectangle({r}, {c})={area} result={result}")    

        return result                   
                                        
        
        