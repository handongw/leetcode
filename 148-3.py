# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import Optional
        
DEBUG = False
        
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        ''' sort linked list using bottom up merge sort. 
            solution: merge sort linked list in place.
            TC: O(n log n),   SC: O(1)
        '''
        if head is None:
            return None


        def print_list(head, label):
            items = []
            while head:
                items.append(head.val)
                head = head.next
            print(f"{label} {items}")    

        dummy_head = ListNode(0, head) # smallest node value
        dummy_tail = ListNode(0)  # largest node value
        p = head
        n = 0
        while p:
            n += 1
            if p.next is None:
                p.next = dummy_tail
                break
            p = p.next   

        # advance p by steps or p reaches dummy_tail
        def advance_ptr(p, steps, include_dummy_tail=True):
            if p == dummy_tail:
                return p

            if include_dummy_tail:    
                while steps > 0 and p != dummy_tail:
                    p = p.next
                    steps -= 1
                return p   
            else:
                while steps > 0 and p.next != dummy_tail:
                    p = p.next
                    steps -= 1
                return p

        # prev_ptr => next_ptr
        # [left_head, ..., left_tail]
        # [right_head, ..., right_tail]
        def merge_in_place(prev_ptr, left_head, left_tail, right_head, right_tail, next_ptr):
            tmp_head = ListNode()
            tmp_tail = tmp_head

            px = left_head
            py = right_head

            while px is not None and py is not None: # both sub lists have remaining nodes
                if py.val < px.val:
                    tmp_tail.next = py
                    tmp_tail = tmp_tail.next
                    py = py.next
                else: # stable sort. just advance px and p0
                    tmp_tail.next = px
                    tmp_tail = tmp_tail.next
                    px = px.next

            if px is not None:
                tmp_tail.next = px
                tmp_tail = left_tail
            else:    
                tmp_tail.next = py
                tmp_tail = right_tail

            # insert (tmp_head, tmp_tail] after prev_ptr
            tmp_tail.next = next_ptr
            prev_ptr.next = tmp_head.next

            return tmp_tail    



        # sort nodes start from head
        width = 1
        while width < n:
            # start another round of merge sub lists with length=width
            if DEBUG:
                print(f"    merge sub list width={width}")

            for i in range(0, n, width*2):
                # prev_ptr -> [left_head, ..., left_tail] -> [right_head, ..., right_tail] -> next_ptr
                if i==0:  # start of round
                    prev_ptr  = dummy_head
                else:
                    prev_ptr  = right_tail

                left_head = advance_ptr(prev_ptr, 1, include_dummy_tail=False)
                left_tail = advance_ptr(left_head, width-1, include_dummy_tail=False)
        
                right_head = advance_ptr(left_tail, 1, include_dummy_tail=True)                   
                if right_head == dummy_tail:
                    break  # it is done for this width

                right_tail = advance_ptr(right_head, width-1, include_dummy_tail=False)
                next_ptr  = advance_ptr(right_tail, 1, include_dummy_tail=True)

                # detach [left_head, ..., left_tail]
                left_tail.next = None

                # detach [right_head, ..., right_tail]
                right_tail.next = None

                prev_ptr.next = next_ptr
                    
                if DEBUG:    
                    print_list(dummy_head, f'        before partial merge width={width} p0={prev_ptr.val} p11={left_head.val} p12={left_tail.val} p21={right_head.val} p22={right_tail.val} p3={next_ptr.val}')
                right_tail = merge_in_place(prev_ptr, left_head, left_tail, right_head, right_tail, next_ptr)
                if DEBUG:
                    print_list(dummy_head, f'        after partial merge width={width} p0={prev_ptr.val} p11={left_head.val} p12={left_tail.val} p21={right_head.val} p22={right_tail.val} p3={next_ptr.val}')

            width *= 2    

        # remove dummy head and dummy tail
        p = dummy_head
        while p.next != dummy_tail:
            p = p.next
        p.next = None
        return dummy_head.next                    