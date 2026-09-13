from typing import List
from collections import deque
import copy

class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:

        def flatten_state(state: List[List[int]]) -> List[int]:
            return [x for row in state for x in row]

        def state_to_str(state: List[int]) -> str:
            return "".join([str(x) for x in state])


        flatten_board = flatten_state(board)
        board_zero_index = flatten_board.index(0)
        end_state = flatten_state( [[1,2,3], [4,5,0]])
        neighbors = (
            (1, 3),
            (0, 2, 4),
            (1, 5),
            (0, 4),
            (1, 3, 5),
            (2, 4),
        )           

        def is_end_state(state: List[int]):
            # print(f"        isEndState {state}: {state == end_state}")
            return state == end_state


        def next_states(state: List[int], zero_index) :
            nextStates = []

            for i in neighbors[zero_index]:
                new_state = state.copy()
                new_state[i] = 0
                new_state[zero_index] = state[i]

                nextStates.append((new_state, i))

            return nextStates        

        # initialize BFS
        visited = set[str]()
        q = deque()  # [(state, zero_index, depth)]

        q.append((flatten_board, board_zero_index, 0))
        visited.add(state_to_str(flatten_board))


        while q:
            state, zero_index, depth = q.popleft()

            if is_end_state(state):
                return depth

            for new_state, new_zero_index in next_states(state, zero_index):
                new_state_str = state_to_str(new_state)
                if not new_state_str in visited:
                    q.append((new_state, new_zero_index, depth+1))
                    visited.add(new_state_str)

        return -1            

