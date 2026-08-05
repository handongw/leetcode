# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import Optional

DEBUG = False


class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        '''
            Repeatedly move the node after the original left node to the front
            of the reversing section. 
            
            O(n) time and O(1) extra space.
        '''

        if left == right:
            return head

        dummy = ListNode(-100, head)  # provides a predecessor when left == 1

        before_left = dummy
        for _ in range(left-1):
            before_left = before_left.next
        
        left_ptr = before_left.next
        if DEBUG:
            print(f"    before_left node={before_left.val} left node={left_ptr.val}")    

        for _ in range(left, right):
            # Detach the node immediately after left_ptr.
            after_left = left_ptr.next
            left_ptr.next = after_left.next
            # Insert the detached node immediately after before_left.
            after_left.next = before_left.next
            before_left.next = after_left

        return dummy.next

def linkedlist_to_array(head):
    result = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result    

def array_to_linkedlist(nums):
    head = None
    for v in reversed(nums):
        head = ListNode(v, head)
    return head    

if __name__ == '__main__':
    sol = Solution()

    DEBUG = True

    head = [1,2,3,4,5]
    left = 2
    right = 4
    expected = [1,4,3,2,5]    
    print(f"head={head} left={left} right={right}")
    output = linkedlist_to_array(sol.reverseBetween(array_to_linkedlist(head), left, right))
    print(f"   expected={expected}")
    print(f"   output  ={output}")
    print(f"   {'PASS' if output==expected else 'FAIL'}\n\n")


    head = [1,2,3,4,5]
    left = 1
    right = 4
    expected = [4,3,2,1,5]    
    print(f"head={head} left={left} right={right}")
    output = linkedlist_to_array(sol.reverseBetween(array_to_linkedlist(head), left, right))
    print(f"   expected={expected}")
    print(f"   output  ={output}")
    print(f"   {'PASS' if output==expected else 'FAIL'}\n\n")



    head = [1,2,3,4,5]
    left = 2
    right = 5
    expected = [1,5, 4,3,2]    
    print(f"head={head} left={left} right={right}")
    output = linkedlist_to_array(sol.reverseBetween(array_to_linkedlist(head), left, right))
    print(f"   expected={expected}")
    print(f"   output  ={output}")
    print(f"   {'PASS' if output==expected else 'FAIL'}\n\n")

