class Solution:
    def can_sum(self, target_sum, numbers):
        if target_sum == 0:
            return True
        if target_sum < 0 or not numbers:
            return False
        peek = numbers[-1]
        f1 = self.can_sum(target_sum - peek, numbers)
        if f1:
            return True
        return self.can_sum(target_sum, numbers[:-1])
