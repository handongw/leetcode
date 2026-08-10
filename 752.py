from collections import deque
from typing import List

class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        
        def split_lock_str(s):
            digits = []
            for c in s:
                digits.append(int(c))
            return (digits[0], digits[1], digits[2], digits[3])

        target_digits = split_lock_str(target)
        deadends_digits = set()
        for s in deadends:
            if s == '0000':
                return -1
            deadends_digits.add(split_lock_str(s))

        if target == '0000':
            return 0

        visited = [ [  [ [False]*10 for _ in range(10)] for _ in range(10) ] for _ in range(10)  ]
        
        q = deque()
        q.append(((0,0,0,0), 0))
        visited[0][0][0][0] = True


        def rotate_wheel(i):
            n1 = (i + 1) % 10
            n2 = (i - 1 )
            if n2 < 0: 
                n2 = 9
            return [n1, n2]     

        while q:
            u, dist = q.popleft()
            if u == target_digits:
                return dist

            adjacents = []
            # rotate wheel 0
            for digit in rotate_wheel(u[0]):
                v = (digit, u[1], u[2], u[3])
                if not visited [v[0]][v[1]][v[2]][v[3]] and not v in deadends_digits:
                    adjacents.append(v)


            # rotate wheel 1
            for digit in rotate_wheel(u[1]):
                v = (u[0], digit, u[2], u[3])
                if not visited [v[0]][v[1]][v[2]][v[3]] and not v in deadends_digits:
                    adjacents.append(v)

            # rotate wheel 2
            for digit in rotate_wheel(u[2]):
                v = (u[0], u[1], digit, u[3])
                if not visited [v[0]][v[1]][v[2]][v[3]] and not v in deadends_digits:
                    adjacents.append(v)

            # rotate wheel 3
            for digit in rotate_wheel(u[3]):
                v = (u[0], u[1], u[2], digit)
                if not visited [v[0]][v[1]][v[2]][v[3]] and not v in deadends_digits:
                    adjacents.append(v)

            # print(f"u={u} adjacents={adjacents}")
            for v in adjacents:                
                visited [v[0]][v[1]][v[2]][v[3]] = True
                q.append((v, dist+1))


        return -1