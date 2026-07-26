# There are n cars on an infinitely long road. The cars are numbered from 0 to n - 1 from left to right and each car is present at a unique point.

# You are given a 0-indexed string directions of length n. directions[i] can be either 'L', 'R', or 'S' denoting whether the ith car is moving towards the left, towards the right, or staying at its current point respectively. Each moving car has the same speed.

# The number of collisions can be calculated as follows:

# When two cars moving in opposite directions collide with each other, the number of collisions increases by 2.
# When a moving car collides with a stationary car, the number of collisions increases by 1.
# After a collision, the cars involved can no longer move and will stay at the point where they collided. Other than that, cars cannot change their state or direction of motion.

# Return the total number of collisions that will happen on the road.

# Constraints:

# 1 <= directions.length <= 105
# directions[i] is either 'L', 'R', or 'S'.

from collections import deque


class Solution:
    def countCollisions(self, directions: str) -> int:
        history=[]
        answer = 0

        q = deque(directions)  # more flexible than list to simulate various scencarios

        # check track from left to right
        while q:
            c = q.popleft()

            if c == 'L':  # <--
                if len(history) > 0:
                    top = history.pop()
                    if top == 'R':
                        answer += 2
                        q.appendleft('S')  # two cars collide and stopped
                    elif top == 'S':
                        answer += 1
                        q.appendleft('S')  # c collide with top and stopped
                    else:
                        pass  # wont happen        
                else:    
                    pass # ignore this car
            elif c == 'R':
                history.append(c)                
            elif c == 'S':
                if len(history) > 0:
                    peek = history[len(history)-1]
                    # top = history.pop()
                    if peek == 'R':
                        history.pop()
                        answer += 1
                        q.appendleft('S') # in case there are more --> cars in history
                    elif peek == 'S':
                        pass # keep one S
                    else:
                        pass # wont happen        
                else:
                    if len(history) == 0 or history[len(history)-1] != 'S':                    
                        history.append('S')
            else:
                raise Exception(f'Invalid direction {c}')

        return answer


if __name__ == '__main__':
    import sys
    import time

    DEBUG = False
    selected_tests = None  # None: run all; else set of 1-based indices from argv

    for a in sys.argv[1:]:
        if a == "-d":
            DEBUG = True
        elif a.replace(",", "").isdigit() and "," in a:
            if selected_tests is None:
                selected_tests = set()
            for part in a.split(","):
                part = part.strip()
                if part.isdigit():
                    selected_tests.add(int(part))
        elif a.isdigit():
            if selected_tests is None:
                selected_tests = set()
            selected_tests.add(int(a))
        else:
            print(
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 4)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    tests = [
        {"n": 1, "directions": "RLRSLL", "expected": 5},
        {"n": 2, "directions": "LLRR", "expected": 0},
        {"n": 3, "directions": "RLRSLL", "expected": 5},
        {"n": 4, "directions": "RRRLS", "expected": 4},
        {"n": 5, "directions": "SLLLSSSRRRL", "expected": 7},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        directions = test["directions"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} directions={directions!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.countCollisions(directions)
            if result != expected:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {test['n']} OK: (result={result})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
 