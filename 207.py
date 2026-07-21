from collections import deque
from typing import List

# There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
# You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

# For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
# Return true if you can finish all courses. Otherwise, return false.

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:

        prerequisite_map = {}
        dependency_map = {}
        for i in range(numCourses):
            prerequisite_map[i] = set()
            dependency_map[i] = []

        candidate_set = set(range(numCourses))
        for e in prerequisites:
            ai, bi = e
            prerequisite_map[ai].add(bi)
            dependency_map[bi].append(ai)            
            candidate_set.discard(ai)

        queue = deque(candidate_set)
        complete_cnt = 0
        while len(queue) > 0:
            c = queue.popleft()
            complete_cnt += 1
            for dep_course in dependency_map[c]:
                prerequisite_map[dep_course].remove(c)
                if len(prerequisite_map[dep_course]) == 0:
                    queue.append(dep_course)


        return complete_cnt == numCourses

