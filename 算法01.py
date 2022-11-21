#leetcode:239
# 输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
# 输出：[3,3,5,5,6,7]
# 解释：
# 滑动窗口的位置                最大值
# ---------------               -----
# [1  3  -1] -3  5  3  6  7       3
#  1 [3  -1  -3] 5  3  6  7       3
#  1  3 [-1  -3  5] 3  6  7       5
#  1  3  -1 [-3  5  3] 6  7       5
#  1  3  -1  -3 [5  3  6] 7       6
#  1  3  -1  -3  5 [3  6  7]      7


nums = [1,3,-1,-3,5,3,6,7]
k = 3

class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        if not nums:return []
        windows,res=[],[]
        for i,x in enumerate(nums):
            print(i,k)
            if i>=k and windows[0] <=i-k:
                windows.pop(0)
            while windows and nums[windows[-1]] <=x:
                windows.pop()
            windows.append(i)
            if i >= k-1:
                res.append(nums[windows[0]])
        return res

s=Solution()
print(s.maxSlidingWindow(nums,k))

kk="aa"
a={"a":1,"b":2,"c":3}
# a["kk"]=kk
# print(a)

def aa(a:dict,kk):
    a["kk"]=kk
    print(a)
    return a

print(aa(a,kk))
