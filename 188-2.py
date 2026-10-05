from typing import List
DEBUG = True

# O(kn) solution
class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)

        # dp[r][d] = max profit of first d days under max r transactions.
        # 0<=d<=n;   0<=r<=k
        dp = [ [ 0 for _ in range(n+1)] for _ in range(k+1)]

        for r in range(1, k+1):
            # max_diff = max(dp[r-1][b] - prices[b]) = max of
            #   dp[r-1][0]   - prices[0]
            #   dp[r-1][1]   - prices[1]
            #   ........................
            #   dp[r-1][d-2] - prices[d-2]

            max_diff = 0 
            for d in range(2, n+1): # it is not possible to sell in < 2 days
                # no sell at (d-1)th day
                no_sell_profit = dp[r][d-1]

                # sell at (d-1)th day
                sell_price = prices[d-1]
                # sell profit = max(dp[r-1][b] + sell_price - prices[b]) 
                #             = max(dp[r-1][b] - prices[b]) + sell_price
                # where 0 <= b <= d-2. b is index of last buy day
                max_diff = max(max_diff, dp[r-1][d-2] - prices[d-2])
                sell_profit = max_diff + sell_price

                dp[r][d] = max(no_sell_profit, sell_profit)
        if DEBUG:
            for r in range(k+1):
                print(f"dp[{r}]={dp[r]}")
                
        return dp[k][n]