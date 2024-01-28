class Solution:
    def merge(
        self, nums1: list[int], m: int, nums2: list[int], n: int
    ) -> None:
        m -= 1
        n -= 1

        while m >= 0 and n >= 0:
            if nums1[m] > nums2[n]:
                val = nums1[m]
                m -= 1
            else:
                val = nums2[n]
                n -= 1

            nums1[m + n + 2] = val

        if n >= 0:
            nums1[: n + 1] = nums2[: n + 1]
