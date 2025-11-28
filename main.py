import time #to get the time NOW
import tracemalloc #to track memory usage
import random #will use it to get random samples
import pandas as pd #data manipulation
import matplotlib.pyplot as plt #to plot the results
import numpy as np

#Bubble sort Alg
def bubbleSort(arr, key=None): #if there is key it will sort according to it
    # Copy data to experment on it freely:)
    #if array is numby array copy it, else convert to numby array because it's faster
    if isinstance(arr, np.ndarray):
        data = arr.copy()
    else:
        data = np.array(arr)
    
    n = len(data) #size
    
    if n <= 1:
        return data
    
    for i in range(n): #normal bubble sorting function
        swapped = False
        
        for j in range(n-1, i, -1):
            if key is not None: #sort with key if there is (key is coulmn we want to sort according to it)
                first = data[j][key]
                second = data[j - 1][key]
            else:
                first = data[j]
                second = data[j - 1]
            if first < second:
                data[j], data[j - 1] = data[j - 1], data[j]
                swapped = True
        
        if not swapped:
            break
    
    return data


#Quick sort Alg
def quickSort(arr, key=None):

    if len(arr) <= 1:
        return arr.copy()
    
    pivot = arr[len(arr) // 2] # this // means give the result as integer because index can't be float
    pivot_value = pivot[key] if key else pivot
    
    left = []
    middle = []
    right = []
    
    for item in arr:
        item_value = item[key] if key else item
        
        if item_value < pivot_value:
            left.append(item)
        elif item_value == pivot_value:
            middle.append(item)
        else:
            right.append(item)
    
    return quickSort(left, key) + middle + quickSort(right, key)

#print(quickSort([2,5,1,5,-5,-4,3])) بس عشان اتأكد
#print(bubbleSort([2,5,1,5,-5,-4,3]))

