# 冒泡排序
"""
比较相邻的元素。如果第一个比第二个大，就交换他们两个。

对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。

针对所有的元素重复以上的步骤，除了最后一个。

持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较

"""

# def bubbleSort(arr):
#     # 遍历除最后一个数之外的所有数
#     for i in range(1, len(arr)):
#         # 随机遍历一个数
#         for j in range(0, len(arr) - i):
#             if arr[j] > arr[j + 1]:
#                 arr[j], arr[j + 1] = arr[j + 1], arr[j]
#                 print(arr)
#
#     return arr
#
#
# bubbleSort([1, 2, 6, 4, 9, 8, 11, 22, 32])

# 选择排序
"""
首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。

再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。

重复第二步，直到所有元素均排序完毕。
"""


# def selectsion(arr):
#     for i in range(len(arr) - 1):
#         # 记录最小数的索引
#         mindex = i
#         for j in range(i + 1, len(arr)):
#             if arr[j] < arr[mindex]:
#                 mindex = j
#
#         # i 不是最小数时，将i和最小数交换
#         if i != mindex:
#             arr[i], arr[mindex] = arr[mindex], arr[i]
#     print(arr)
#
#     return arr
#
#
# selectsion([2, 7, 8, 1, 5, 6, 42, 45])

# 插入排序
"""
将第一待排序序列第一个元素看做一个有序序列，把第二个元素到最后一个元素当成是未排序序列。

从头到尾依次扫描未排序序列，将扫描到的每个元素插入有序序列的适当位置。（如果待插入的元素与有序序列中的某个元素相等，则将待插入元素插入到相等元素的后面。）

"""

#
# def insertion(arr):
#     for i in range(len(arr)):
#         preindex = i - 1
#         current = arr[i]
#         while preindex >= 0 and arr[preindex] > current:
#             arr[preindex + 1] = arr[preindex]
#             # 刷新每个数的索引值
#             preindex -= 1
#         arr[preindex + 1] = current
#     print(arr)
#     return arr
#
#
# insertion([2, 1, 6, 4, 5, 8, 9, 45, 16])

# 希尔排序
"""
选择一个增量序列 t1，t2，……，tk，其中 ti > tj, tk = 1；

按增量序列个数 k，对序列进行 k 趟排序；

每趟排序，根据对应的增量 ti，将待排序列分割成若干长度为 m 的子序列，分别对各子表进行直接插入排序。仅增量因子为 1 时，整个序列作为一个表来处理，表长度即为整个序列的长度。
"""


def shellsoft(arr):
    import math
    gap = 1
    while (gap < len(arr) / 3):
        gap = gap * 3 + 1
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i - gap
            while j >= 0 and arr[j] > temp:
                arr[j + gap] = arr[j]
                j -= gap
            arr[j + gap] = temp
        gap = math.floor(gap / 3)
    print(arr)
    return arr


shellsoft([2, 1, 5, 6, 8, 7, 9, 45])
