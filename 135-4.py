DEBUG = False

# TC O(n) two directional scans; SC O(n)
class Solution:
    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)

        candies = [1 for _ in range(n)]

        # scan left to right
        for i in range(1, n):
            if ratings[i] > ratings[i-1]:
                candies[i] = candies[i-1] + 1
        if DEBUG:
            print(f"left-right scan: candies={candies}")        

        # scan right to left
        for j in range(n-2, -1, -1):
            if ratings[j] > ratings[j+1]:
                candies[j] = max(candies[j], candies[j+1]+1) 
        if DEBUG:
            print(f"right-left scan: candies={candies}")                  

        total_candies = 0
        for m in candies:
            total_candies += m
        return total_candies
