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

# ===========================================
# ⏱️ 3. MEASURE TIME AND MEMORY
# ===========================================

def measure_performance(algorithm, data, key=None, algorithm_name=""):
    """
    ⏱️ Measure algorithm performance (time + memory)
    """
    tracemalloc.start()
    start_time = time.perf_counter()
    
    sorted_data = algorithm(data.copy(), key)
    
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time_ms = (end_time - start_time) * 1000
    memory_kb = peak / 1024
    
    print(f"⏱️ {algorithm_name}: {execution_time_ms:.2f} ms | 🧠 Memory: {memory_kb:.1f} KB")
    
    return execution_time_ms, memory_kb, sorted_data

# ===========================================
# 📊 4. DATASET PROCESSING FUNCTIONS
# ===========================================

def load_and_prepare_your_dataset(csv_path):
    """
    📊 Load and prepare YOUR actual dataset from Kaggle
    """
    print(f"📁 Loading your dataset from: {csv_path}")
    
    # Load your CSV file
    dataFile = pd.read_csv(csv_path)
    
    print(f"✅ Dataset loaded: {len(dataFile)} records, {len(dataFile.columns)} columns")
    print("📋 Columns available:")
    for i, col in enumerate(dataFile.columns, 1):
        print(f"   {i}. {col}")
    
    # Convert to list of dictionaries for sorting
    data_dict = dataFile.to_dict('records')
    
    return dataFile, data_dict

def create_test_scenarios_from_your_data(data_dict, dataFile):
    """
    🎯 Create realistic test scenarios from YOUR dataset
    """
    scenarios = {}
    
    # Scenario 1: Full dataset
    scenarios['full_dataset'] = data_dict
    
    # Scenario 2: Sorted by price (best case for Bubble Sort)
    if 'Price' in dataFile.columns:
        scenarios['sorted_by_price'] = sorted(data_dict, key=lambda x: x.get('Price', 0))
    
    # Scenario 3: Random sample
    scenarios['random_sample'] = random.sample(data_dict, min(1000, len(data_dict)))
    
    # Scenario 4: Reverse sorted by price (worst case for Bubble Sort)
    if 'Price' in dataFile.columns:
        scenarios['reverse_sorted_price'] = sorted(data_dict, key=lambda x: x.get('Price', 0), reverse=True)
    
    # Scenario 5: Small subset
    scenarios['small_subset'] = data_dict[:100]
    
    # Scenario 6: By ticket type if available
    if 'Ticket Type' in dataFile.columns:
        ticket_types = dataFile['Ticket Type'].unique()[:2]  # First 2 types
        for ticket_type in ticket_types:
            type_data = [item for item in data_dict if item.get('Ticket Type') == ticket_type]
            if len(type_data) > 10:
                scenarios[f'ticket_type_{ticket_type}'] = type_data
    
    return scenarios

# ===========================================
# 🚀 5. MAIN COMPARISON FUNCTION
# ===========================================

def run_complete_analysis_on_your_data(csv_path):
    """
    🚀 Run complete analysis on YOUR Kaggle dataset
    """
    print("🚀 COMPLETE ALGORITHM ANALYSIS ON YOUR DATASET")
    print("=" * 60)
    
    # Load YOUR dataset
    dataFile, data_dict = load_and_prepare_your_dataset(csv_path)
    
    # Create test scenarios from your data
    scenarios = create_test_scenarios_from_your_data(data_dict, dataFile)
    
    results = []
    
    # Find available columns for sorting
    sort_columns = []
    if 'Price' in dataFile.columns:
        sort_columns.append('Price')
    elif 'price' in dataFile.columns:
        sort_columns.append('price')
    else:
        # Use first numeric column
        numeric_cols = dataFile.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            sort_columns.append(numeric_cols[0])
    
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
                bubble_time, bubble_memory, bubble_sorted = measure_performance(
                    bubbleSort, scenario_data, sort_col, "BUBBLE SORT"
                )
                
                # Test Quick Sort
                quick_time, quick_memory, quick_sorted = measure_performance(
                    quickSort, scenario_data, sort_col, "QUICK SORT"
                )
                
                # Determine winner
                winner = "BUBBLE" if bubble_time < quick_time else "QUICK"
                improvement = max(bubble_time, quick_time) / min(bubble_time, quick_time)
                
                print(f"   🏆 Winner: {winner} | 📈 Improvement: {improvement:.1f}x")
                
                # Store results
                results.append({
                    'scenario': scenario_name,
                    'sort_column': sort_col,
                    'bubble_time_ms': bubble_time,
                    'quick_time_ms': quick_time,
                    'bubble_memory_kb': bubble_memory,
                    'quick_memory_kb': quick_memory,
                    'winner': winner,
                    'improvement_ratio': improvement,
                    'data_size': len(scenario_data)
                })
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    return results, dataFile

# ===========================================
# 📈 6. VISUALIZATION AND REPORTING
# ===========================================

thePath = "cleaned_data.csv"  # ← UPDATE THIS PATH

try:
    # Run complete analysis on YOUR dataset
    results, dataFile = run_complete_analysis_on_your_data(thePath)
    
    if results:
        # Create visualization
        create_simple_visualization(results)
        
        # Generate final report
        generate_final_report(results, dataFile)
        
        print(f"\n✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print(f"📊 Check the generated chart: results_comparison.png")
    
except FileNotFoundError:
    print(f"❌ File not found: {thePath}")
    print("⚠️ Please update the file path in the main() function")
except Exception as e:
    print(f"❌ Error: {e}")
