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


def dataAnalysisFunction():

    print("\n\n\n\t<<ALGORITHMS ANALYSIS!!>>\n\n")
    print("==================================")
    
    # load test scenarios from the data
    scenarios = testScenarios()
    
    results = []
    
    if not sort_columns: #if no append habben to the sort_columns list
        print("No good columns found for sorting")
        return

    for sort_col in sort_columns:
        print(f"\nSorting by: {sort_col}!")
        print("-" * 40)
        
        #* scenarios is dict, name is the key and data is the value!
        for scenario_name, scenario_data in scenarios.items():
            if len(scenario_data) < 2:
                continue
            
            print(f"\nScenario: {scenario_name}")
            print(f"   -Records: {len(scenario_data)}")
            
            try:
                # Test Bubble Sort
                bubble_time, bubble_memory = measure_time_space(
                    scenario_data, sort_col, "Bubble Sort"
                )
                
                # Test Quick Sort
                quick_time, quick_memory = measure_time_space(
                    scenario_data, sort_col, "Quick Sort"
                )
                
                # Determine winner
                winner = "BUBBLE" if bubble_time < quick_time else "QUICK"
                improvement = max(bubble_time, quick_time) / min(bubble_time, quick_time)
                print('~'*30)
                print(f"\n\n\t!!!  Winner: {winner} |  Improvement: {improvement:.1f}x  !!!\n\n")
                print('~'*30)
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
                print(f"    Error: {e}")
                continue
    
    return results


def create_simple_visualization(results, output_file="results_comparison.png"):
    """
    📈 Create simple visualization of results
    """
    if not results:
        print("❌ No results to visualize")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Prepare data
    scenarios = [f"{r['scenario']}\n({r['data_size']} rec)" for r in results]
    bubble_times = [r['bubble_time_ms'] for r in results]
    quick_times = [r['quick_time_ms'] for r in results]
    
    x = range(len(scenarios))
    width = 0.35
    
    plt.bar([i - width/2 for i in x], bubble_times, width, label='Bubble Sort', color='red', alpha=0.7)
    plt.bar([i + width/2 for i in x], quick_times, width, label='Quick Sort', color='blue', alpha=0.7)
    
    plt.xlabel('Test Scenarios')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title('Bubble Sort vs Quick Sort Performance on Your Dataset')
    plt.xticks(x, scenarios, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📊 Visualization saved as: {output_file}")


def generate_final_report(results, dataFile):

    if not results:
        print("No results to report")
        return
    
    print("\n" + "=" * 60)
    print("FINAL ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"\nDataset Summary:")
    print(f"   Total Records: {len(dataFile):,}")
    print(f"   Total Columns: {len(dataFile.columns)}")
    print(f"   Total Test Scenarios: {len(results)}")
    
    # Calculate wins
    bubble_wins = sum(1 for r in results if r['winner'] == 'BUBBLE')
    quick_wins = sum(1 for r in results if r['winner'] == 'QUICK')
    # the iterative var is 'r'
    # if the key in the results dict is winner and the valuse of it is XXXAlgXXX add 1 to xxx_Wins
    print('='*20)
    print(f"\n\tPerformance Summary:")
    print(f" Bubble Sort Wins: {bubble_wins}")
    print(f" Quick Sort Wins: {quick_wins}")
    print(f"\n <<Best Overall: {'Bubble Sort' if bubble_wins >= quick_wins else 'Quick Sort'}>>")
    
    # Show best and worst cases
    best_improvement = max(results, key=lambda x: x['improvement_ratio'])
    worst_improvement = min(results, key=lambda x: x['improvement_ratio'])

    print('='*20)
    print(f"\n\tBest Case for Quick Sort:")
    print(f" Scenario: {best_improvement['scenario']}")
    print(f" Improvement: {best_improvement['improvement_ratio']:.1f}x faster")

    print('='*20)
    print(f"\n\tWorst Case for Quick Sort:")
    print(f" Scenario: {worst_improvement['scenario']}")
    print(f" Improvement: {worst_improvement['improvement_ratio']:.1f}x faster")

#the MAIN code

print(f"dataset path: {thePath}")
print(f"Dataset contain: {len(dataFile)} records, {len(dataFile.columns)} columns")#print records and columns
print("Columns available:")#print names of the columns
for i, column in enumerate(dataFile.columns, 1):
    print(f"\t{i}.\t{column}")

# Convert to list of dictionaries for sorting
data_dict = dataFile.to_dict('records')

try:
    # Run complete analysis on YOUR dataset
    results = dataAnalysisFunction()
    
    if results:
        # Create visualization
        create_simple_visualization(results)
        
        # Generate final report
        generate_final_report(results, dataFile)
        
        print(f"\nThe end~")
        print(f"Check the generated chart: results_comparison.png")
    
except FileNotFoundError:
    print(f"File not found\wrong path: {thePath}")
    print("Please update the file path in the globals block")
except Exception as e:
    print(f"Error: {e}")


