# Author  : SAI BALACHANDAR V

import time
import random

def time_logger(func):
    """
    Function to measure the execution time of any given function.
    """
    def wrapper_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Time taken:", end_time - start_time, "seconds")
        return result
    return wrapper_func

def log_writer(func):
    """
    Function to log the status of the fucntion Execution"
    """
    def wrapper_log(*args, **kwargs):
        with open('log.txt', 'a') as file:
            file.write("Function started: " + func.__name__ + "\n")    # --------> get the function name using __name__ and write it to Log.
        result = func(*args, **kwargs)                                 # --------> The function passed as a input to decorator will be called and executed here.
        with open('log.txt', 'a') as file:
            file.write("Function ended: " + func.__name__ + "\n")
        return result
    return wrapper_log
    
# time_logger → log_writer → compute_average this how the decorator works while execution

@time_logger    
@log_writer    
def compute_average(data):
    """
    Function to compute the average value of a list of numbers.
    """
    total = sum(data)
    avg = total / len(data)
    return avg


# Example usage
numbers = [random.randint(1, 100) for _ in range(1000000)] #This will create a list of random numbers from 1 to 100 with list lenght of 1000000.
average = compute_average(numbers)
print("Average value is:", average)
