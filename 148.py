# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import Optional
        
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        ''' sort linked list using bottom up merge sort. 
            solution: convert linked list to node array for fast access.
            TC: O(n log n),   SC: O(n)
        '''
        if head is None:
            return None

        ptrList = []   # store pointers in array for fast access
        p = head
        while p:
            ptrList.append(p)
            p = p.next
        n = len(ptrList)

        mergePtrList = [None] * n # store merge result

        def merge(lo, m, hi):
            i = lo
            j = m

            k = lo
            while i<m and j<hi:
                if ptrList[i].val > ptrList[j].val:
                    mergePtrList[k]= ptrList[j]
                    j += 1
                else:
                    mergePtrList[k] = ptrList[i]
                    i += 1
                k += 1  
            
            while i<m:
                    mergePtrList[k] = ptrList[i]
                    k += 1
                    i += 1
                
            while j < hi:
                mergePtrList[k] = ptrList[j]
                k += 1
                j += 1                   


        width = 1 # size of sub list to be merged

        while width < n:
            for lo in range(0, n, width*2):
                # calc two sub list index
                # ptrList[lo:m], ptrList[m:hi]
                m = min(n, lo+width)
                hi = min(n, m+width)

                merge(lo, m, hi)

            tmp = ptrList    
            ptrList = mergePtrList
            mergePtrList = tmp
                

            width *= 2       

        # construct final linked list as result
        for i in range(n):
            if i < n-1:
                ptrList[i].next = ptrList[i+1]
            else:
                ptrList[i].next = None   
        return ptrList[0]        
