from typing import List

DEBUG = False

class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        parent_dict = {}
        island_count = 0
        movements = [(1,0), (-1,0), (0, 1), (0,-1)]
        answer = []

        if DEBUG:
            print(f"grid={m}x{n} position={positions}")

        # union-and-find root of pos
        def find_root(pos):
            if parent_dict[pos] != pos:
                parent_dict[pos] = find_root(parent_dict[pos])
            return parent_dict[pos]    

        for p in positions:
            new_pos = (p[0], p[1])

            parent = parent_dict.get(new_pos, None)
            if parent is not None:
                if DEBUG:
                    print(f"    {new_pos} appeared before")
                answer.append(island_count)  # no change if islands
                continue

            merge_adj_array = []  # adjacent positions that touch islands
            for mv in movements:
                adjacent = (new_pos[0]+mv[0], new_pos[1]+mv[1])
                if adjacent[0]>=0 and adjacent[0]<m and adjacent[1]>=0 and adjacent[1]<n:                    
                    adj_parent = parent_dict.get(adjacent, None)
                    if adj_parent is not None:
                        merge_adj_array.append(adjacent)

            if len(merge_adj_array) <= 0:
                if DEBUG:
                    print(f"    {new_pos} is a new island")
                parent_dict[new_pos] = new_pos  # new_pos is a new island
                island_count += 1
                answer.append(island_count)
                continue

            first_merge_adj = merge_adj_array[0]
            parent_dict[new_pos] = find_root(first_merge_adj) # new_pos joins existing island
            if DEBUG:
                print(f"   {new_pos} join island {find_root(new_pos)}")

            for remaining_merge_adj in merge_adj_array[1:]:
                if find_root(new_pos) == find_root(remaining_merge_adj):
                    if DEBUG:
                        print(f"    {remaining_merge_adj} and new_pos {new_pos} within same island {find_root(new_pos)}")
                    pass # remaining_merge_adj and new_pos within same island
                else:
                    if DEBUG:
                        print(f"   merge island {find_root(remaining_merge_adj)} to island {find_root(new_pos)}")
                    # merge remaining_merge_adj's island to new_pos's island
                    parent_dict[find_root(remaining_merge_adj)] = find_root(new_pos)
                    island_count -= 1  

            answer.append(island_count)

        return answer    



        