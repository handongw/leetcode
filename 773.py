from typing import List
from collections import deque
import copy

class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        end_state = [[1,2,3], [4,5,0]]
        m = 2
        n = 3

        def isEndState(state: List[List[int]]):
            # print(f"        isEndState {state}: {state == end_state}")
            return state == end_state

        def stateToStr(state: List[List[int]]) -> str:
            return f"{state[0]}{state[1]}"


        def zeroLocation(state: List[List[int]]):
            zero_row = 0

            while zero_row < m:
                zero_col = 0
                while zero_col < n:
                    if state[zero_row][zero_col] == 0:
                        return (zero_row, zero_col)
                    zero_col += 1
                zero_row += 1
            raise Exception(f"invalidate {state}") 

        def nextStates(state: List[List[int]]):
            zero_row, zero_col = zeroLocation(state)

            nextStates = []
            moves = [(-1,0), (1,0), (0,-1), (0, 1)]
            for delta in moves:
                i = zero_row + delta[0]
                j = zero_col + delta[1]

                if i>=0 and i<m and j>=0 and j<n:
                    new_state = copy.deepcopy(state)
                    # swap (i, j) and (zero_row, zero_col)
                    new_state[i][j] = 0
                    new_state[zero_row][zero_col] = state[i][j]
                    # zeroLocation(new_state)
                    nextStates.append(new_state)
            return nextStates        


        visited = set()
        q = deque()  # [(state, depth)]

        q.append((board, 0))
        visited.add(stateToStr(board))


        while q:
            state, depth = q.popleft()

            if isEndState(state):
                return depth

            for new_state in nextStates(state):
                new_state_str = stateToStr(new_state)
                if not new_state_str in visited:
                    q.append((new_state, depth+1))
                    visited.add(new_state_str)

        return -1            

