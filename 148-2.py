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

        dummy_head = ListNode(-(10**6), head) # smallest node value
        dummy_tail = ListNode(10**6)  # largest node value
        p = head
        n = 0
        while p:
            n += 1
            if p.next is None:
                p.next = dummy_tail
                break
            p = p.next   

        # advance p by steps or p reaches dummy_tail
        def advance_ptr(p, steps):
            if p != dummy_tail:
                while steps > 0:
                    p = p.next
                    steps -= 1
                    if p == dummy_tail:
                        break
            return p   

        def merge_in_place(p0, p11, p12, p21, p22, p3):
            px = p11
            py = p21

            # stable state: p0 -> [px, ..., p12] -> [py, ..., p22] -> p3

            while px != py and py != p3: # both sub lists have remaining nodes
                if py.val < px.val:
                    # detach py node
                    p12.next = py.next

                    # insert py after p0 and then advance p0
                    py.next = px
                    p0.next = py

                    # move p0
                    p0 = py

                    py = p12.next
                else: # stable sort. just advance px and p0
                    px = px.next
                    p0 = p0.next

            # no need to handle remaining nodes but need to update and return p22
            p = p0
            while p.next != p3:
                p = p.next
            return p    



        # sort nodes start from head
        width = 1
        while width < n:
            # start another round of merge sub lists with length=width
            if DEBUG:
                print(f"    merge sub list width={width}")

            for i in range(0, n, width*2):
                # p0 -> [p11, ..., p12] -> [p21, ..., p22] -> p3
                if i==0:  # start of round
                    p0  = dummy_head
                else:
                    p0  = p22

                p11 = advance_ptr(p0, 1)
                p12 = advance_ptr(p11, width-1)
                p21 = advance_ptr(p12, 1)
                p22 = advance_ptr(p21, width-1)
                p3  = advance_ptr(p22, 1)
                    
                if DEBUG:    
                    print_list(dummy_head, f'        before partial merge width={width} p0={p0.val} p11={p11.val} p12={p12.val} p21={p21.val} p22={p22.val} p3={p3.val}')
                p22 = merge_in_place(p0, p11, p12, p21, p22, p3)
                if DEBUG:
                    print_list(dummy_head, f'        after partial merge width={width} p0={p0.val} p11={p11.val} p12={p12.val} p21={p21.val} p22={p22.val} p3={p3.val}')

            width *= 2    

        # remove dummy head and dummy tail
        p = dummy_head
        while p.next != dummy_tail:
            p = p.next
        p.next = None
        return dummy_head.next                    