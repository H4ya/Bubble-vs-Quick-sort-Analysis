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


def measure_time_space(data, key=None, algorithm_name=""):
    
    if(algorithm_name=="Bubble Sort"):
        start_time = time.perf_counter() #performance counter (will store the exact starting time)
        tracemalloc.start() #start tracing memory usage
        sorted_data = bubbleSort(data.copy(), key)
    else:
        start_time = time.perf_counter() #performance counter (will store the exact starting time)
        tracemalloc.start() #start tracing memory usage
        sorted_data = quickSort(data.copy(), key)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory() #Maximum memo use from start the trace until now 
    tracemalloc.stop() #stop tracking memo
    
    executionT_ms = (end_time - start_time) * 1000 # second * 1000 = millisecond! thus, this line convert to millisecond
    memoKB = peak / 1024 #convert bytes to KB
    print(f"{algorithm_name} took: {executionT_ms:.2f} ms | 🧠 Memory: {memoKB:.2f} KB")
    
    return executionT_ms, memoKB, sorted_data


def run_complete_analysis_on_your_data():

    print("\n\t\tALGORITHMS ANALYSIS!!")
    print("==================================")
    
    # Load YOUR dataset
    
    # Create test scenarios from the data
    scenarios = testScenarios()
    
    results = []
    
    # Find available columns for sorting
    sort_columns = []

    sort_columns.append('Price')

    if not sort_columns:
        print("❌ No numeric columns found for sorting")
        return
    
    for sort_col in sort_columns:
        print(f"\n🎯 SORTING BY: {sort_col}")
        print("-" * 40)
        
        for scenario_name, scenario_data in scenarios.items():
            if len(scenario_data) < 2:
                continue
                
            print(f"\n📊 Scenario: {scenario_name}")
            print(f"   Records: {len(scenario_data)}")
            
            try:
                # Test Bubble Sort
                bubble_time, bubble_memory, bubble_sorted = measure_time_space(
                    scenario_data, sort_col, "Bubble Sort"
                )
                
                # Test Quick Sort
                quick_time, quick_memory, quick_sorted = measure_time_space(
                    scenario_data, sort_col, "Quick Sort"
                )
                
                # Determine winner
                winner = "BUBBLE" if bubble_time < quick_time else "QUICK"
                improvement = max(bubble_time, quick_time) / min(bubble_time, quick_time)
                
                print(f"\n\n\t🏆 Winner: {winner} | 📈 Improvement: {improvement:.1f}x  !!!")
                
                # Store results
                results.append({
                    'scenario': scenario_name,
                    'sort_column': sort_col,
                    'bubble_time_ms': bubble_time,
                    'quick_time_ms': quick_time,
                    'bubble_memoKB': bubble_memory,
                    'quick_memoKB': quick_memory,
                    'winner': winner,
                    'improvement_ratio': improvement,
                    'data_size': len(scenario_data)
                })
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    return results


