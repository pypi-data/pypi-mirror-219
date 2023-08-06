import numpy as np
from decimal import Decimal

def EuclideanDis(pts1, pts2):
    """
    欧式距离与中心点
    :param pts1: 位置(x1,y1)
    :param pts2: 位置(x2,y2)
    :return: (两点间距离, 中心点)
    """
    distance = ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5
    center = ((pts1[0] + pts2[0]) / 2, (pts1[1] + pts2[1]) / 2)
    return distance, center

def retain(val,t=2):
    value=Decimal(val)
    return round(value,t)

def normal(x, mu, sigma):
    p = 1 / np.sqrt(2 * np.pi * sigma**2)
    return p * np.exp(-0.5 / sigma**2 * (x - mu)**2)

class pysort():
    def insertion_sort(self, arr):
        """
        直接插入排序
        :param arr:
        :return:
        """
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            print(arr)

    def quick_sort(self, arr, low, high):
        """
        快速排序
        :param arr:
        :param low:
        :param high:
        :return:
        """
        if low < high:
            pivot_index = self.partition(arr, low, high)
            print(arr)
            self.quick_sort(arr, low, pivot_index - 1)
            self.quick_sort(arr, pivot_index + 1, high)

    def partition(self, arr, low, high):
        """
        :param arr:
        :param low:
        :param high:
        :return:
        """
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def bubble_sort(self, arr):
        """
        冒泡排序
        :param arr:
        :return:
        """
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            print(arr)

    def selection_sort(self, arr):
        """
        直接选择排序
        :param arr:
        :return:
        """
        n = len(arr)
        for i in range(n - 1):
            min_index = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
            print(arr)
if __name__=="__main__":
    a=[64,45,8,10,70,6]
    Sort=pysort()
    Sort.selection_sort(a)