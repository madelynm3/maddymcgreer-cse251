'''
Requirements
1. Create a multiprocessing program that reads in files with defined tasks to perform.
2. The program should use a process pool per task type and use apply_async calls with callback functions.
3. The callback functions will store the results in global lists based on the task to perform.
4. Once all 4034 tasks are done, the code should print out each list and a breakdown of 
   the number of each task performed.
   
Questions:
1. How many processes did you specify for each pool:
   >Finding primes: 4
   >Finding words in a file: 4
   >Changing text to uppercase: 4
   >Finding the sum of numbers: 4
   >Web request to get names of Star Wars people: 4
   
   >How do you determine these numbers:
   These are determined by the number of CPU cores and the nature of the tasks.

2. Specify whether each of the tasks is IO Bound or CPU Bound?
   >Finding primes: CPU
   >Finding words in a file: I/O
   >Changing text to uppercase: CPU
   >Finding the sum of numbers: CPU
   >Web request to get names of Star Wars people: I/O
   
3. What was your overall time, with:
   >one process in each of your five pools:  __5.2_ seconds
   >with the number of processes you show in question one:  _7.7__ seconds
'''
import glob
import json
import math
import multiprocessing as mp
import os
import time
from datetime import datetime, timedelta

import numpy as np
import requests

TYPE_PRIME = 'prime'
TYPE_WORD = 'word'
TYPE_UPPER = 'upper'
TYPE_SUM = 'sum'
TYPE_NAME = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        result_primes.append(f"{value} is prime")
    else:
        result_primes.append(f"{value} is not prime")


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt") as f:
        if word in f.read():
            result_words.append(f"{word} Found")
        else:
            result_words.append(f"{word} not found *****")


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    result_upper.append(f"{text} ==> {text.upper()}")


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = sum(range(start_value, end_value + 1))
    result_sums.append(f"sum of {start_value:,} to {end_value:,} = {total:,}")


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    try:
        response = requests.get(url)
        name = response.json()['name']
        result_names.append(f"{url} has name {name}")
    except Exception as e:
        result_names.append(f"{url} had an error receiving the information")


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    begin_time = time.time()

    # Create process pools for each task type
    pool_primes = mp.Pool()
    pool_words = mp.Pool()
    pool_upper = mp.Pool()
    pool_sums = mp.Pool()
    pool_names = mp.Pool()

    # List of tasks to be executed asynchronously
    tasks_primes = []
    tasks_words = []
    tasks_upper = []
    tasks_sums = []
    tasks_names = []

    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        task = load_json_file(filename)
        task_type = task['task']
        if task_type == TYPE_PRIME:
            tasks_primes.append(pool_primes.apply_async(task_prime, args=(task['value'],)))
        elif task_type == TYPE_WORD:
            tasks_words.append(pool_words.apply_async(task_word, args=(task['word'],)))
        elif task_type == TYPE_UPPER:
            tasks_upper.append(pool_upper.apply_async(task_upper, args=(task['text'],)))
        elif task_type == TYPE_SUM:
            tasks_sums.append(pool_sums.apply_async(task_sum, args=(task['start'], task['end'])))
        elif task_type == TYPE_NAME:
            tasks_names.append(pool_names.apply_async(task_name, args=(task['url'],)))
        else:
            print(f'Error: unknown task type {task_type}')

    # Wait for all tasks to complete
    for task in tasks_primes:
        task.get()
    for task in tasks_words:
        task.get()
    for task in tasks_upper:
        task.get()
    for task in tasks_sums:
        task.get()
    for task in tasks_names:
        task.get()

    # Close the pools
    pool_primes.close()
    pool_words.close()
    pool_upper.close()
    pool_sums.close()
    pool_names.close()

    # Join the pools
    pool_primes.join()
    pool_words.join()
    pool_upper.join()
    pool_sums.join()
    pool_names.join()

    # Print results
    print('-' * 80)
    print(f'Primes: {len(result_primes)}')
    print('\n'.join(result_primes))

    print('-' * 80)
    print(f'Words: {len(result_words)}')
    print('\n'.join(result_words))

    print('-' * 80)
    print(f'Uppercase: {len(result_upper)}')
    print('\n'.join(result_upper))

    print('-' * 80)
    print(f'Sums: {len(result_sums)}')
    print('\n'.join(result_sums))

    print('-' * 80)
    print(f'Names: {len(result_names)}')
    print('\n'.join(result_names))

    print(f'Number of Primes tasks: {len(result_primes)}')
    print(f'Number of Words tasks: {len(result_words)}')
    print(f'Number of Uppercase tasks: {len(result_upper)}')
    print(f'Number of Sums tasks: {len(result_sums)}')
    print(f'Number of Names tasks: {len(result_names)}')
    print(f'Finished processes {len(task_files)} tasks = {time.time() - begin_time}')


if __name__ == '__main__':
    main()
