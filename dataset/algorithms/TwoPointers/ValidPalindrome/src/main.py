class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        sl = list(s)
        sl = [i for i in sl if i.isalnum()]
        return sl == sl[::-1]
