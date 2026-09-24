from typing import List

DEBUG = False

class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        parent_dict = {}
        island_size_dict = {}

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

        # union islands supports rank/size
        def union_island(pos1, pos2):
            root1 = find_root(pos1)
            root2 = find_root(pos2)

            if root1 != root2:
                # merge smaller island to bigger island
                if island_size_dict[root1] < island_size_dict[root2]:
                    parent_dict[root1] = root2
                    island_size_dict[root2] += island_size_dict[root1]
                else:
                    parent_dict[root2] = root1
                    island_size_dict[root1] += island_size_dict[root2]    
                return True
            else:
                return False        

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

            parent_dict[new_pos] = new_pos  # new_pos be a new island first
            island_size_dict[new_pos] = 1   
            island_count += 1

            for remaining_merge_adj in merge_adj_array:
                # merge remaining_merge_adj's island to new_pos's island
                if union_island(new_pos, remaining_merge_adj):
                    island_count -= 1  

            answer.append(island_count)

        return answer