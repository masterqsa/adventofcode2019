import collections
import copy
import functools
import itertools
import math
import operator
import re
import sys
import typing
from collections import Counter, defaultdict, deque
from typing import List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
        
class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        root = head
        d = dict()
        d[root] = True
        while root.next != None:
            root = root.next
            if root in d:
                return root
            d[root] = True
        return None


    
sol = Solution()
root = ListNode(3)
n1 = ListNode(2)
n2 = ListNode(0)
n3 =  ListNode(-4)
root.next = n1
n1.next = n2
n2.next = n3
n3.next = n1
ret = sol.detectCycle(root)
print(-1 if ret == None else ret.val)
