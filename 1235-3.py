import bisect
from typing import List


class Solution:

  def jobScheduling(
      self, startTime: List[int], endTime: List[int], profit: List[int]
  ) -> int:
    # 1. Zip and sort directly by startTime
    jobs = sorted(zip(startTime, endTime, profit))

    n = len(jobs)
    # Extract sorted start times into a simple list for C-optimized binary search
    start_times = [j[0] for j in jobs]

    # max_profit_dp[i] stores max profit from jobs[i:n] (exact same DP design)
    max_profit_dp = [0] * (n + 1)

    # Fill DP table right-to-left
    for i in range(n - 1, -1, -1):
      job_start, job_end, job_profit = jobs[i]

      # bisect_left replaces the pure-Python binary search loop with C-level code
      k = bisect.bisect_left(start_times, job_end, lo=i + 1)

      # Take current job + future profit VS skip current job
      max_profit_dp[i] = max(job_profit + max_profit_dp[k], max_profit_dp[i + 1])

    return max_profit_dp[0]