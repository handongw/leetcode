from functools import cache
from typing import List

class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = []
        n = len(startTime)
        for i in range(n):
            jobs.append((startTime[i], endTime[i], profit[i]))

        jobs.sort()

        @cache
        def max_profit(start_job_idx):
            if start_job_idx >= n:
                raise Exception(f"invalid job index:{start_job_idx}")
            if start_job_idx == n-1: # last job
                return jobs[start_job_idx][2]

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
                candidate1 = job_profit + max_profit(k)

            return max(candidate1, max_profit(start_job_idx+1))    

        return max_profit(0)            

