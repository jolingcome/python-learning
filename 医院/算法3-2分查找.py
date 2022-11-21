#二分查找的条件：（1）必须是有序（升序或降序） （2）必须有边界
# 数值array, target是要找的数。空间复杂度是n,时间复杂度是log2n
def check(array,target):
    left,right=0,len(array)-1
    while left<right:
        mid=(left+right)/2
        if array[mid]==target:
            break #或者return result
        elif array[mid]<target: # target在右半边
            left=mid+1 #左边界移到mid后面一格，然后再次循环while语句
        else:
            right=mid-1


