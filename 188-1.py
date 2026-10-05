from typing import List
from functools import cache

# O(k n ^ 2) solution
class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)

        # max_buy_sell_profit[start_idx][sell_day]: 
        # max profit of (a) buying at [start_idx, sell_day) (b) sell at sell_day
        # profit <= 0 means no buy-sell can make profit
        # O(n ^ 2)
        max_buy_sell_profit = [ [ 0 for _ in range(n)] for _ in range(n)]
        for sell_day in range(n-1, 0, -1):
            best_profit = 0
            for buy_day in range(sell_day-1, -1, -1):
                diff = prices[sell_day] - prices[buy_day]
                best_profit = max(best_profit, diff)
                max_buy_sell_profit[buy_day][sell_day] = best_profit


        # remain_k: number of transactions avaiable
        # start_idx: start index of prices
        # return max profit
        @cache
        def max_profit(remain_k:int, start_idx:int) -> int:
            if remain_k <=0:
                return 0
            if start_idx >= n-1:
                return 0
            
            # try various next sell days after start_idx
            best_candidate_profit = -1
            candidates = []

            def add_candidate(profit, new_start_idx):
                nonlocal best_candidate_profit
                if profit > best_candidate_profit:
                    candidates.append((profit, new_start_idx))
                    best_candidate_profit = profit
                # else skip later new_start_idx whose profit < previous profit    

            result = 0
            for sell_day in range(start_idx+1, n):
                profit = max_buy_sell_profit[start_idx][sell_day]
                # result = max(result, profit + max_profit(remain_k-1, sell_day+1))
                add_candidate(profit, sell_day+1)

            for profit, new_start_idx in candidates:
                result = max(result, profit + max_profit(remain_k-1, new_start_idx))

            #     if profit > 0:
            #         result = max(result, profit + max_profit(remain_k-1, sell_day+1))
            #     else:
            #         result = max(result, max_profit(remain_k, sell_day+1))
            # # try advance start_idx without sell        
            # result = max(result, max_profit(remain_k, start_idx+1))
            return result

        return max_profit(k, 0)
