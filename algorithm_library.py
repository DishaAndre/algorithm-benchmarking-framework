import math
from typing import List

# ==========================================
# SORTING ALGORITHMS
# ==========================================

def bubble_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def selection_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr: List[int]) -> List[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def quick_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    sorted_arr = quick_sort(left) + middle + quick_sort(right)
    for i in range(len(arr)):
        arr[i] = sorted_arr[i]
    return arr

def counting_sort(arr: List[int]) -> List[int]:
    if not arr: return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)
    
    for num in arr:
        count[num] += 1
        
    i = 0
    for a in range(max_val + 1):
        for _ in range(count[a]):
            arr[i] = a
            i += 1
    return arr

def radix_sort(arr: List[int]) -> List[int]:
    if not arr: return arr
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        
        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1
            
        for i in range(1, 10):
            count[i] += count[i - 1]
            
        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1
            
        for i in range(n):
            arr[i] = output[i]
        exp *= 10
    return arr

# ==========================================
# SEARCHING ALGORITHMS
# ==========================================

def linear_search(arr: List[int], target: int) -> int:
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr: List[int], target: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def jump_search(arr: List[int], target: int) -> int:
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
            
    while prev < min(step, n) and arr[prev] <= target:
        if arr[prev] == target:
            return prev
        prev += 1
        
    return -1

def fibonacci_search(arr: List[int], target: int) -> int:
    n = len(arr)
    if n == 0:
        return -1
        
    fibMMm2 = 0 
    fibMMm1 = 1 
    fibM = fibMMm2 + fibMMm1 
    
    while fibM < n:
        fibMMm2 = fibMMm1
        fibMMm1 = fibM
        fibM = fibMMm2 + fibMMm1
        
    offset = -1
    
    while fibM > 1:
        i = min(offset + fibMMm2, n - 1)
        
        if arr[i] < target:
            fibM = fibMMm1
            fibMMm1 = fibMMm2
            fibMMm2 = fibM - fibMMm1
            offset = i
        elif arr[i] > target:
            fibM = fibMMm2
            fibMMm1 = fibMMm1 - fibMMm2
            fibMMm2 = fibM - fibMMm1
        else:
            return i
            
    if fibMMm1 and offset < n - 1 and arr[offset + 1] == target:
        return offset + 1
        
    return -1

# ==========================================
# COMPLEXITY METADATA
# ==========================================

COMPLEXITIES = {
    "Bubble Sort": {"best": "O(n)", "avg": "O(n^2)", "worst": "O(n^2)", "space": "O(1)"},
    "Selection Sort": {"best": "O(n^2)", "avg": "O(n^2)", "worst": "O(n^2)", "space": "O(1)"},
    "Insertion Sort": {"best": "O(n)", "avg": "O(n^2)", "worst": "O(n^2)", "space": "O(1)"},
    "Merge Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"},
    "Quick Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n^2)", "space": "O(log n)"},
    "Counting Sort": {"best": "O(n+k)", "avg": "O(n+k)", "worst": "O(n+k)", "space": "O(n+k)"},
    "Radix Sort": {"best": "O(nk)", "avg": "O(nk)", "worst": "O(nk)", "space": "O(n+k)"},
    "Linear Search": {"best": "O(1)", "avg": "O(n)", "worst": "O(n)", "space": "O(1)"},
    "Binary Search": {"best": "O(1)", "avg": "O(log n)", "worst": "O(log n)", "space": "O(1)"},
    "Jump Search": {"best": "O(1)", "avg": "O(√n)", "worst": "O(√n)", "space": "O(1)"},
    "Fibonacci Search": {"best": "O(1)", "avg": "O(log n)", "worst": "O(log n)", "space": "O(1)"}
}