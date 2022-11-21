#leetcode 2
# 输入：nums = [2,7,11,15], target = 9
# 输出：[0,1]
# 解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1]

#题解：（1）暴力解法时间复杂度是O(n^2)
#      (2) 用hash,set和map都是hash,再用target-x看是不是在hash里面，只有一次循环时间复杂度O(n)


#使用第二种写法
class Solution(object):
    def towSum(self,nums,target):
        for i,number in nums:
            print(i,number)
            if target-number in nums:
                pass
                # return [i,target-]

nums = [2,7,11,15]
target = 18

a=Solution()
result=a.towSum(nums=nums,target=target)
print(result)

# class Solution:
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
#         hashtable = dict()
#         for i, num in enumerate(nums):
#             if target - num in hashtable:
#                 return [hashtable[target - num], i]
#             hashtable[nums[i]] = i
#         return []


