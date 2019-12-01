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

order = defaultdict(int)
class Solution:
    def alienOrder(self, words: List[str]) -> str:
        
        letters = set()
        pre = defaultdict(set)
        post = defaultdict(set)
        for w in words:
            for c in w:
                letters.add(c)
        for i, w in enumerate(words):
            if i < len(words) - 1:
                l = min(len(words[i]), len(words[i+1]))
                j = 0
                while j < l and words[i][j] == words[i+1][j]:
                    j+=1
                if j < l:
                    post[words[i][j]].add(words[i+1][j])
                    pre[words[i+1][j]].add(words[i][j])
                
        free = letters - set(pre)
        order = ''
        while free:
            a = free.pop()
            order += a
            for b in post[a]:
                pre[b].discard(a)
                if not pre[b]:
                    free.add(b)
        return order * (set(order) == letters)
    
sol = Solution()
print(sol.alienOrder([
    "z",
    "z"
#   "wrt",
#   "wrf",
#   "er",
#   "ett",
#   "rftt",
  #"wee"
]))