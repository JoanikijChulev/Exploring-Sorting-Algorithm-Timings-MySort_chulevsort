

#Joanikij Chulev
#This algorithm preformed most satisfactory.



import random
import time

import threading

def find_min(input_list, min_values):
    while input_list:
        min_value = min(input_list)
        min_values.append(min_value)
        input_list.remove(min_value)

def find_max(input_list, max_values):
    while input_list:
        max_value = max(input_list)
        max_values.append(max_value)
        input_list.remove(max_value)

def split_list(input_list):
    mean_value = sum(input_list) / len(input_list)
    lower_values = [x for x in input_list if x < mean_value]
    higher_values = [x for x in input_list if x >= mean_value]
    return lower_values, higher_values

def chulevsort(input_list):
    lower_values, higher_values = split_list(input_list)

    min_values = []
    max_values = []


    min_thread = threading.Thread(target=find_min, args=(lower_values, min_values))
    max_thread = threading.Thread(target=find_max, args=(higher_values, max_values))

    min_thread.start()
    max_thread.start()

    min_thread.join()
    max_thread.join()

    max_values.reverse()

    sorted_list = min_values + max_values

    return sorted_list





#Testing code


input_list = [random.randint(-1000, 1000) for _ in range(10000)]
# Measure execution time
start_time = time.time()
sorted_list = chulevsort(input_list)
end_time = time.time()

# Print the sorted list (you can comment this line if you don't want to see the sorted list)


# Print the execution time
execution_time = end_time - start_time
print(f"Execution Time: {execution_time:.6f} seconds")


