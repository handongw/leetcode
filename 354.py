from typing import List

DEBUG = False

class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        envelopes.sort()  # sort by width and then height. width and height can have duplicate values

        heights = sorted(set(h for _, h in envelopes))
        # map actual height to natural number, i.e 1, 2, 3, ...
        rank_map = {h: i + 1 for i, h in enumerate(heights)}
        N = len(heights)        

        if DEBUG:
            print(f"height_map={rank_map}")

        # Use Fenwick tree to track max layers by height
        BIT = [0] * (N+1)         

        # max layers of russion doll whose height < curr_h
        def prev_max_layers(curr_h):
            curr_rank = rank_map[curr_h]
            if curr_rank <=1:
                return 0

            max_layers = 0
            rank = curr_rank - 1
            while rank>=1:
                max_layers = max(max_layers, BIT[rank])
                rank -= (rank & -rank)
            return max_layers

        # update max russian doll layers for h >= curr_h
        def update_prev_max_layer2(curr_h, max_layers):
            rank = rank_map[curr_h] 
            while rank <= N:
                BIT[rank] = max(max_layers, BIT[rank])
                rank += (rank & -rank)


        last_w = envelopes[0][0]
        g_start_idx=0
        n = len(envelopes)
        global_max_layers = 1
        group_max_layers = []
        while g_start_idx < n:
            g_end_idx = g_start_idx
            while g_end_idx < n and envelopes[g_end_idx][0] == last_w:
                group_max_layers.append((envelopes[g_end_idx], prev_max_layers(envelopes[g_end_idx][1])+1  ))
                g_end_idx += 1
                
            for e, max_layer in group_max_layers:
                h = e[1]
                if DEBUG:
                    print(f"    e={e} max_layer={max_layer}")
                update_prev_max_layer2(h, max_layer)
                global_max_layers = max(global_max_layers, max_layer)
            group_max_layers.clear()    

            g_start_idx = g_end_idx                                
            if g_end_idx < n:
                last_w = envelopes[g_end_idx][0]

        return global_max_layers    
# Constraints:

# 1 <= envelopes.length <= 105
# envelopes[i].length == 2
# 1 <= wi, hi <= 105        