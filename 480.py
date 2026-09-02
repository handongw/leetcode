from typing import List
import heapq
DEBUG = False

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if DEBUG:
            print(f"nums={nums} k={k}")
        if k == 1:
            return nums[:]

        sliding_window = [(nums[i], i) for i in range(k)]
        sliding_window.sort()
        result = []

        hi = k // 2
        k_is_odd = k % 2 > 0
        # k_is_even = k % 2 == 0
        if DEBUG:
            print(f"k={k} hi={hi} sliding_window={sliding_window}")

        if k_is_odd:
            result.append(sliding_window[hi][0])
        else:
            result.append((sliding_window[hi-1][0] + sliding_window[hi][0])/2)

        # if k is even, split sliding window into two equal parts.
        # if k is odd, split slidng windows into two equal parts (excluding the medium number)
        # invarant: left_side <= right_side
        left_side = [ (-sliding_window[i][0], sliding_window[i][1])  for i in range(hi)]     # logical max heap
        right_side = [ (sliding_window[i][0], sliding_window[i][1]) for i in range(hi, k)] # min heap

        left_idx_set = set[int]()   # keep track of effective index of left side
        right_idx_set = set[int]()  # keep track of effective index of right side
        for x in left_side:
            left_idx_set.add(x[1])
        for x in right_side:
            right_idx_set.add(x[1])    

        heapq.heapify(left_side)
        heapq.heapify(right_side)

        if DEBUG:
            print(f"result={result}\n")

        def peek_left_side(window_start):
            if len(left_side) <= 0:
                return None
            # reach top    
            top = left_side[0]
            while top[1] < window_start:
                heapq.heappop(left_side)
                if len(left_side) <= 0:
                    return None
                top = left_side[0]
            return (-top[0], top[1]) # convert it to positive value
    
        def push_left_side(x):
            heapq.heappush(left_side, (-x[0], x[1]))
                       
        def peek_right_side(window_start):
            if len(right_side) <= 0:
                return None
            # reach top    
            top = right_side[0]
            while top[1] < window_start:
                heapq.heappop(right_side)
                if len(right_side) <= 0:
                    return None
                top = right_side[0]    
            return top               

        window_start = 0
        for i in range(k,len(nums)):
            if DEBUG:
                print(f"curr window={nums[window_start:window_start+k]}")
                print(f"next window={nums[window_start+1:window_start+k+1]}")
            ins_v = nums[i]
            left_top = peek_left_side(window_start)
            right_top = peek_right_side(window_start)
            if DEBUG:
                print(f"start left_top={left_top}:{len(left_idx_set)}=>{left_idx_set} right_top={right_top}:{len(right_idx_set)}=>{right_idx_set} v={ins_v} index={i}")
                print(f"start end left_top={left_side} right_top={right_side}")


            if ins_v <= right_top[0]: # add nums[i] to left
                if DEBUG:
                    print(f"    add nums[{i}] to left")
                push_left_side((ins_v, i))
                left_idx_set.add(i)
            else: # ins_v > right_top[0] add nums[i] to right
                if DEBUG:
                    print(f"    add nums[{i}] to right")
                heapq.heappush(right_side, (ins_v, i))
                right_idx_set.add(i)

            left_idx_set.discard(window_start)
            right_idx_set.discard(window_start)
            if DEBUG:
                print(f"    left_idx_set={left_idx_set} right_idx_set={right_idx_set}")

            # Rebalance active elements:
            # odd k:  len(right_idx_set) == len(left_idx_set) + 1
            # even k: len(right_idx_set) == len(left_idx_set)            window_start += 1
            left_top = peek_left_side(window_start)
            right_top = peek_right_side(window_start)
            if DEBUG:
                print(f"    left size={len(left_idx_set)} right size={len(right_idx_set)}")
            if k_is_odd:    
                if len(left_idx_set) + 1 < len(right_idx_set):
                    if DEBUG:
                        print(f"    move right_top to left_side")
                    heapq.heappop(right_side)
                    push_left_side(right_top)
                    left_idx_set.add(right_top[1])
                    right_idx_set.remove(right_top[1])
                elif len(left_idx_set) >= len(right_idx_set):
                    if DEBUG:
                        print(f"    move left_top to right_side")
                    heapq.heappop(left_side)
                    heapq.heappush(right_side, left_top)    
                    right_idx_set.add(left_top[1])
                    left_idx_set.remove(left_top[1])
            else: # k is even
                if len(left_idx_set) < len(right_idx_set):
                    if DEBUG:
                        print(f"    move right_top to left_side")
                    heapq.heappop(right_side)
                    push_left_side(right_top)
                    left_idx_set.add(right_top[1])
                    right_idx_set.remove(right_top[1])
                elif len(left_idx_set) > len(right_idx_set):
                    if DEBUG:
                        print(f"    move left_top to right_side")
                    heapq.heappop(left_side)
                    heapq.heappush(right_side, left_top)    
                    right_idx_set.add(left_top[1])
                    left_idx_set.remove(left_top[1])


            left_top = peek_left_side(window_start)
            right_top = peek_right_side(window_start)
            if DEBUG:
                print(f"end left_top={left_side} right_top={right_side}")

            if k_is_odd:
                result.append(right_top[0])
            else:
                result.append((left_top[0] + right_top[0])/2)

            if DEBUG:
                print(f"result={result}\n")

        return result
        