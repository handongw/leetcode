from typing import List
import math

DEBUG = False


def get_full_mask(n):
    bits = 0x1
    while n > 1:
        bits = bits <<1 | 0x1
        n -= 1
    return bits    

def numToBit(n):
    if n == 0:
        return 0x1
    else:
        return 0x1 << n

def lowest_set_bit(p):
    if p == 0:
        return 0
    return p & -p

def bitPatternToStr(bitPattern, size):
    return bin(bitPattern)[2:].zfill(size)

def splitBitPattern(pattern):
    bitList = []
    while pattern:
        bit = pattern & -pattern
        bitList.append(bit)
        pattern &= pattern - 1  
    return bitList 

def flipBitPattern(pattern, n):
    """Treat pattern as an n-bit pattern and flip all bits.  (~p) & ((1 << n) - 1)"""
    mask = (1 << n) - 1
    return (~pattern) & mask

    

def conflict(pos1, pos2):
    # print(f"  pos1={pos1}  pos2={pos2}")

    if pos1[0] == pos2[0] or pos1[1] == pos2[1]: 
        return True
    return abs(pos1[0]-pos2[0]) == abs(pos1[1]-pos2[1])

def printBoard(matrix):            
    for row in matrix:
        print(' '.join(row))
    print()

def saveBoardToFile(matrix, fileName):   
    """append matrix to the given file"""         
    with open(fileName, 'a', encoding='utf-8') as f:
        for row in matrix:
            f.write(' '.join(row) + '\n')
        f.write('\n\n')

def removeBoardFile(fileName):
    """delete the board result file"""
    from pathlib import Path
    Path(fileName).unlink(missing_ok=True)

def create_board(n):
    return  [["." for j in range(n)] for i in range(n)]

def bits_to_str(b, n):
    return bin(b)[2:].zfill(n)

def col_bit_list_to_str_list(col_bit_list, n):
    return [bits_to_str(col_bit, n) for col_bit in col_bit_list]


class Solution:



    def solveNQueens(self, n: int) -> List[List[str]]:
        result_set = set()

        def playQueen(row_bits, left_diag_mask, right_diag_mask, steps, results):
            if DEBUG:
                print(f" playQueen row_bits={bits_to_str(row_bits,n)} left_diag_mask={bits_to_str(left_diag_mask,n)} right_diag_mask={bits_to_str(right_diag_mask,n)} steps={col_bit_list_to_str_list(steps, n)} ")
                
            if len(steps) == n:
                board = create_board(n)
                q_col_list = []
                for row_idx, col_bit in enumerate(steps):
                    col_idx = col_bit.bit_length() - 1
                    q_col_list.append(col_idx)
                    # if DEBUG:
                    #     print(f"  pos={(row_idx, col_idx)} board={board}")
                    board[row_idx][col_idx] = 'Q'
                solution = ["".join(row) for row in board]
                if DEBUG:
                    print(f" find a solution: {solution}")
                    printBoard(board)

                key = frozenset(solution)
                if key not in result_set:    
                    results.append(solution)                        
                else:
                    result_set.add(key)    
                return


            masked_row_bits = row_bits & ~left_diag_mask & ~right_diag_mask
            if DEBUG:
                print(f"masked row bits={bits_to_str(masked_row_bits, n)}")

            col_bit_list = splitBitPattern(masked_row_bits)
            if DEBUG:
                print(f"print_col_bit_list:{col_bit_list_to_str_list(col_bit_list, n)}")

            for col_bit in col_bit_list:
                # if len(steps) == 0 and col_bit.bit_length() > math.ceil(n/2):
                #     continue  # this is symetric

                next_left_diag_mask = left_diag_mask<<1 | col_bit << 1
                next_right_diag_mask = right_diag_mask>>1 | col_bit >> 1
                next_row_bits = row_bits & ~col_bit
                next_steps = steps[:]
                next_steps.append(col_bit)

                playQueen(row_bits=next_row_bits, left_diag_mask=next_left_diag_mask, right_diag_mask=next_right_diag_mask,steps=next_steps, results=results)
            return


        results = []

        playQueen(row_bits=get_full_mask(n), left_diag_mask=0, right_diag_mask=0, steps=[], results=results)

        return results       