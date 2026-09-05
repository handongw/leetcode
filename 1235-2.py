from functools import cache
from typing import List

class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = []
        n = len(startTime)
        for i in range(n):
            jobs.append((startTime[i], endTime[i], profit[i]))

        jobs.sort()

        max_profit_dp = [ 0 for _ in range(n) ] # max profit of jobs[i:n]
        for start_job_idx in reversed(range(n)):
            if start_job_idx==n-1:
                max_profit_dp[start_job_idx] = jobs[start_job_idx][2]
                continue

            job_start_time, job_end_time, job_profit = jobs[start_job_idx]

            # find the first job index k where k>start_job_index, jobs[k]'s start time >= job_end_time
            lo = start_job_idx+1
            hi = n-1
            k = n
            while lo <= hi:
                mid = (lo+hi) // 2
                if jobs[mid][0] >= job_end_time:
                    k = min(k, mid)
                    hi = mid - 1
                else:
                    lo = mid + 1

            if k == n:
                candidate1 = job_profit
            else:
                candidate1 = job_profit + max_profit_dp[k]
            
            # print(f"start_job_idx={start_job_idx} n={n}")
            max_profit_dp[start_job_idx] = max(candidate1, max_profit_dp[start_job_idx+1])


        return max_profit_dp[0]            

