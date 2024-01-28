class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        counter = 0
        p = 0

        for i, n in enumerate(nums[1:]):
            p2 = i + 1

            if nums[p] == n:
                counter += 1
                if counter < 2:
                    p += 1
                    if p2 - p >= 1:
                        nums[p] = n

            if nums[p] != n:
                if counter >= 2:
                    p += 1
                    nums[p] = n
                else:
                    p += 1
                    if p2 - p >= 1:
                        nums[p] = n

                counter = 0

        return p + 1
