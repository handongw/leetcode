# A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

# Every adjacent pair of words differs by a single letter.
# Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
# sk == endWord
# Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words [beginWord, s1, s2, ..., sk].

from collections import deque
from functools import cache
from typing import List

DEBUG = False

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        wlen = len(beginWord)        

        # Build word adjacent data structure
        adjacent_map = {}

        @cache
        def gen_adjacent_map_keys(w):
            chars = list(w)
            keys = []
            for i in range(len(w)):
                c = chars[i]
                chars[i] = '*'
                key = "".join(chars)
                keys.append(key)
                chars[i] = c  # restore chars 
            return keys    

        word_set = set[str](wordList)
        if endWord not in word_set:
            return []

        word_set.add(beginWord)
        word_set.add(endWord)

        for w in word_set:
            for key in gen_adjacent_map_keys(w):
                adjacent_map.setdefault(key, []).append(w)  

        if DEBUG:
            for k in adjacent_map.keys():
                print(f"adjacent_map[{k}]={adjacent_map[k]}")        
        # print(f" adjacent_map={adjacent_map}")
        # {'*ot': ['hot', 'dot', 'lot'], 
        #  'h*t': ['hot'], 
        #  'ho*': ['hot'], 
        #  'd*t': ['dot'], 
        #  'do*': ['dot', 'dog'], 
        #  '*og': ['dog', 'log', 'cog'], 
        #  'd*g': ['dog'], 
        #  'l*t': ['lot'], 
        #  'lo*': ['lot', 'log'], 
        #  'l*g': ['log'], 
        # 'c*g': ['cog'], 
        # 'co*': ['cog']
        # }    

        state = { w: (float('inf'), [])  for w in word_set} # key: word, value: (min-steps, backword-vertex)
        state[beginWord] = (0, [])

        queue = deque()
        queue.append((beginWord, 0)) # (word, steps)

        while queue:
            w, steps = queue.popleft()

            if w == endWord:
                continue
            
            for k in gen_adjacent_map_keys(w):
                for next_w in adjacent_map[k]:
                    if next_w != w:
                        new_step = steps + 1
                        if new_step < state[next_w][0]:
                            state[next_w] = (new_step, [w])
                            queue.append((next_w, new_step))
                        elif new_step == state[next_w][0]:
                            state[next_w][1].append(w)    
        
        if DEBUG:
            for k in state.keys():
                print(f"state[{k}]={state[k]}")

        if state[endWord][0] == float('inf'):
            return []
        else:
            ans = []

            # def gather_path(path):
            #     w = path[0]
            #     if not state[w][1]:
            #         ans.append(list(path)) # append a copy
            #         return
            #     for prev_w in state[w][1]:
            #         # Using deque or appendleft/popleft avoids O(N) list concatenation
            #         path.appendleft(prev_w)
            #         gather_path(path)    
            #         path.popleft() # backtrack

            def gather_path(path):
                w = path[0]
                if not state[w][1]:
                    ans.append(path)
                    return path
                for prev_w in state[w][1]:
                    gather_path([prev_w]+path)    

            gather_path([endWord])
            return ans     


if __name__ == '__main__':
    import sys
    import time

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
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 10 11 12)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")


    tests = [
        { "beginWord": "hit", 
          "endWord": "cog", 
          "wordList": ["hot","dot","dog","lot","log","cog"],
          "expected": [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]],
          "n": 1
        },
        # beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
        #  beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]Output: 0
        { "beginWord": "hit", 
          "endWord": "cog", 
          "wordList": ["hot","dot","dog","lot","log"],
          "expected": [],
          "n": 2
        },
        { "beginWord": "a", 
          "endWord": "c", 
          "wordList": ["a","b","c"],
          "expected": [["a","c"]],
          "n": 3
        },
        #  [['hit', 'hot', 'hog', 'cog']]
        { "beginWord": "hit", 
          "endWord": "cog", 
          "wordList": [
                            "hot", "dot", "dog", "lot", "log", "cog", 
                            "hat", "bat", "bot", "bog", "bit", "big", 
                            "pig", "pug", "mug", "bug", "bag", "tag", 
                            "tig", "hag", "hug" 
                            # Removed "hog" to eliminate the length-4 shortcut
                        ],
          "expected": [
                            ["hit", "hot", "dot", "dog", "cog"],
                            ["hit", "hot", "lot", "log", "cog"],
                            ["hit", "hot", "bot", "bog", "cog"],
                            ["hit", "bit", "big", "bog", "cog"],
                            ['hit', 'bit', 'bot', 'bog', 'cog']
                        ],
          "n": 3
        },
        { "beginWord": "hot", 
          "endWord": "dog", 
          "wordList": ["hot","dog"],
          "expected": [],
          "n": 4
        },
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    def compare_paths(result: list[list[str]], expected: list[list[str]]) -> bool:
        # Convert inner lists to tuples so they can be stored in a set
        set_result = {tuple(path) for path in result}
        set_expected = {tuple(path) for path in expected}
    
        same = set_result == set_expected
        if not same:
            print(f" exists in result only: {set_result - set_expected}")
            print(f" exists in expect only: {set_expected - set_result}")
        return same

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        beginWord = test["beginWord"]
        endWord = test["endWord"]
        wordList = test["wordList"]
        expected = test["expected"]

        expected.sort()

        try:
            print(f"\nTEST {test['n']} test={test} ")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.findLadders(beginWord, endWord, wordList)
            result.sort()
            print(f"  got:      {result}")
            print(f"  expected: {expected}")
            if not compare_paths(result, expected):
                print(f"test {test['n']} FAIL")
            else:
                print(f"test {test['n']} OK")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")