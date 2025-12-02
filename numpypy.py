import csv

data = []
with open('cleaned_data.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['Price'] = float(row['Price'])
        data.append(row)

def bubble_sort_stable(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j]['Price'] > arr[j + 1]['Price']:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

sorted_data = bubble_sort_stable(data)

print("---- Sorted Result (First 20 rows) ----")
for row in sorted_data[:20]:
    price = row.get("Price", "")
    departure = row.get("Departure Time", "")
    print(f"{price} - {departure}")