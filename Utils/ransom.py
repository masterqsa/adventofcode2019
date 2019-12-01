from collections import defaultdict

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        dic = defaultdict(int)
        for c in magazine:
            dic[c]+=1
            
        for c in ransomNote:
            if dic[c] == 0:
                return False
            dic[c]-=1
        return True
    

sol = Solution()
print(sol.canConstruct("aac", "aaaab"))
        
        