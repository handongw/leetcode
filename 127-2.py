# A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

# Every adjacent pair of words differs by a single letter.
# Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
# sk == endWord
# Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

# Constraints:

# 1 <= beginWord.length <= 10
# endWord.length == beginWord.length
# 1 <= wordList.length <= 5000
# wordList[i].length == beginWord.length
# beginWord, endWord, and wordList[i] consist of lowercase English letters.
# beginWord != endWord
# All the words in wordList are unique.

from typing import List

DEBUG = False

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        wlen = len(beginWord)        

        # Build word adjacent data structure
        adjacent_map = {}
        state_map = {}

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

        for w in wordList:
            for key in gen_adjacent_map_keys(w):
                adjacent_map.setdefault(key, []).append(w)            
            state_map[w] = 0 # 0 = unvisited

        if state_map.get(endWord) is None:
            return 0

        if wlen == 1:
            return 2    

        # Handle beginWord not being in wordList smoothly
        if state_map.get(beginWord) is None:
            for key in gen_adjacent_map_keys(beginWord):
                adjacent_map.setdefault(key, []).append(beginWord)            
            state_map[beginWord] = 1 

        # Initialize the two frontiers as Sets
        set1 = {beginWord}
        set2 = {endWord}
        state_map[beginWord] = 1
        state_map[endWord] = 2 

        if DEBUG:
            print(f" adjacent map={adjacent_map}")    

        queue1_steps = 1  
        queue2_steps = 1  

        while set1 and set2:
            # OPTIMIZATION: Always expand the smaller frontier to curb exponential growth
            if len(set1) > len(set2):
                set1, set2 = set2, set1
                queue1_steps, queue2_steps = queue2_steps, queue1_steps
                # We also need to know which numeric state represents our CURRENT expanding frontier
                # If beginWord's initial element is in set1, current_state is 1, else 2.
                # However, checking state_map of an arbitrary element is cleaner:
                any_word = next(iter(set1))
                current_state = state_map[any_word]
            else:
                any_word = next(iter(set1))
                current_state = state_map[any_word]

            target_state = 2 if current_state == 1 else 1
            next_set = set()

            for w in set1:
                if DEBUG:
                    print(f"Processing {w} | current_state={current_state} | steps={queue1_steps}")
                
                for key in gen_adjacent_map_keys(w):
                    # FIX: Safely grab candidates with .get() to avoid KeyErrors
                    candidates = adjacent_map.get(key, [])
                    for candidate in candidates:
                        st = state_map[candidate]
                        if st == 0:
                            next_set.add(candidate)
                            state_map[candidate] = current_state
                        elif st == target_state:
                            # Intersection found!
                            if DEBUG:
                                print(f"Intersection found at {candidate}")   
                            return queue1_steps + queue2_steps

            set1 = next_set
            queue1_steps += 1           
            
        return 0
        
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
          "expected": 5,
          "n": 1
        },
        #  beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]Output: 0
        { "beginWord": "hit", 
          "endWord": "cog", 
          "wordList": ["hot","dot","dog","lot","log"],
          "expected": 0,
          "n": 2
        },
        { "beginWord": "a", 
          "endWord": "c", 
          "wordList": ["a","b","c"],
          "expected": 2,
          "n": 3
        },
        { "beginWord": "hit", 
          "endWord": "cog", 
          "wordList": ["hot","cog","dot","dog","hit","lot","log"],
          "expected": 5,
          "n": 3
        },
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        beginWord = test["beginWord"]
        endWord = test["endWord"]
        wordList = test["wordList"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} test={test} ")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.ladderLength(beginWord, endWord, wordList)
            if result != expected:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {test['n']} OK: (sequence len={result})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")