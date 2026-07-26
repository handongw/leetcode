# You are given the head of a linked list. Delete the middle node, and return the head of the modified linked list.
# The middle node of a linked list of size n is the ⌊n / 2⌋th node from the start using 0-based indexing, where ⌊x⌋ denotes the largest integer less than or equal to x.
# For n = 1, 2, 3, 4, and 5, the middle nodes are 0, 1, 1, 2, and 2, respectively.

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import Optional


class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # Constraints:

    # The number of nodes in the list is in the range [1, 105].
    # 1 <= Node.val <= 105

        # figure out list length
        p = head
        n = 0
        while p is not None:
            n += 1
            p = p.next

        # calc middle node index
        m  = n // 2

        if m == 0:
            return head.next
        
        if m == n-1:
            p = head
            i = 0
            while i< m-1:
                p = p.next
                i += 1
            p.next = None
            return head

        p = head
        i = 0
        while i<m-1:
            p = p.next
            i += 1
        p.next = p.next.next    


        return head


def build_list(vals):
    """Build a linked list from a Python list."""
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head):
    """Convert a linked list to a Python list."""
    result = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


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
        {"n": 1, "head": [1, 3, 4, 7, 1, 2, 6], "expected": [1, 3, 4, 1, 2, 6]},
        {"n": 2, "head": [1, 2, 3, 4], "expected": [1, 2, 4]},
        {"n": 3, "head": [2, 1], "expected": [2]},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        head_vals = test["head"]
        expected = test["expected"]
        head = build_list(head_vals)

        try:
            print(f"\nTEST {test['n']} head={head_vals!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = to_list(solution.deleteMiddle(head))
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
