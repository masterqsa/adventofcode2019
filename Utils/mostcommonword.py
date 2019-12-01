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

class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        d = defaultdict(int)
        b = dict.fromkeys(banned)
        max = 0
        max_key = ""
        for word in re.findall(r"[a-zA-Z]+", paragraph):
            word = word.lower()
            if word not in b:
                d[word] += 1
                if d[word] > max:
                    max = d[word]
                    max_key = word

        return max_key
    
sol = Solution()
print(sol.mostCommonWord("Bob hit a ball, the hit BALL flew far after it was hit.", ["hit"]))