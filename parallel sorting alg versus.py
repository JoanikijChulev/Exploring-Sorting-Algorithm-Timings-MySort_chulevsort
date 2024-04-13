#MY CODE
from random import randint
import random
import time
import concurrent.futures  # used for concurency in the algs



# Function to generate a random array
def generate_random_array(size):
    return [random.randint(-10000, 10000) for _ in range(size)]

# Function to measure the execution time of a parallel sorting algorithm
def measure_execution_time(sort_function, arr):
    start_time = time.time()
    sorted_array = sort_function(arr.copy())
    end_time = time.time()
    return end_time - start_time


#MY CODE





#ALL THE SORTING ALGOTIRHMS WERE TAKEN AS STATED IN THE PAPER(ADJUSTED ALGORHTIMS FOR PARALLELISM)

# Parallel sorting algorithms to compare

def merge(left, right):
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left

    result = []
    index_left = index_right = 0

    while len(result) < len(left) + len(right):
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break

    return result

# Function to perform parallel merge sort
def parallel_merge_sort(arr):
    # If the input array contains fewer than two elements,
    # then return it as the result of the function
    if len(arr) < 2:
        return arr

    midpoint = len(arr) // 2

    # Split the array into two halves
    left_half = arr[:midpoint]
    right_half = arr[midpoint:]

    # Use concurrent.futures.ThreadPoolExecutor to run merge_sort in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Recursively sort the left and right halves in parallel
        left_sorted = executor.submit(parallel_merge_sort, left_half).result()
        right_sorted = executor.submit(parallel_merge_sort, right_half).result()

    # Merge the sorted halves together and return the result
    return merge(left_sorted, right_sorted)









def partition(array):
    if len(array) < 2:
        return array

    low, same, high = [], [], []
    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        if item < pivot:
            low.append(item)
        elif item == pivot:
            same.append(item)
        elif item > pivot:
            high.append(item)

    return low, same, high

def quick_sort(array):
    if len(array) < 2:
        return array

    low, same, high = partition(array)

    return quick_sort(low) + same + quick_sort(high)

def parallel_quick_sort(array):
    if len(array) < 2:
        return array

    low, same, high = partition(array)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create tasks to sort the low and high partitions concurrently
        future_low = executor.submit(quick_sort, low)
        future_high = executor.submit(quick_sort, high)

        # Wait for the tasks to complete and retrieve the results
        sorted_low = future_low.result()
        sorted_high = future_high.result()

    # Combine the sorted low, same, and high partitions
    return sorted_low + same + sorted_high










#MY CODE

# Experiment parameters
array_size = 100000 # Larger array size for this experiment
num_runs = 5

random_array = generate_random_array(array_size)

parallel_algorithm_runtimes = {}  

# Perform the experiment and measure execution times
for sort_func in [parallel_merge_sort, parallel_quick_sort]:
    runtimes = []  # List to store execution times for each run
    for _ in range(num_runs):
        execution_time = measure_execution_time(sort_func, random_array)
        runtimes.append(execution_time)
        print(f"{sort_func.__name__}: Run {len(runtimes)} - Execution Time = {execution_time:.6f} seconds")
    average_time = sum(runtimes) / num_runs
    parallel_algorithm_runtimes[sort_func.__name__] = average_time
    print(f"{sort_func.__name__}: Average Execution Time = {average_time:.6f} seconds")

# Determine the winner (algorithm with the lowest average execution time)
winner = min(parallel_algorithm_runtimes, key=parallel_algorithm_runtimes.get)
print(f"The winner is {winner} with an average execution time of {parallel_algorithm_runtimes[winner]:.6f} seconds")


#MY CODE