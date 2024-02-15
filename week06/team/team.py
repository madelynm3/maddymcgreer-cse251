"""
Course: CSE 251
Lesson Week: 05
File: team05.py
Author: Brother Comeau (modified by Brother Foushee)

Purpose: Team Activity

Instructions:

- See in Canvas

"""

import threading
from threading import Thread, Barrier
from queue import Queue
import queue
import time
import requests
import json

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(thread_index: int, data_queue: Queue, print_queue: Queue, names: list, barrier: Barrier):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        # print(f"{threading.current_thread().name}: before calling get\n, ends=""") -Debugging
        url = data_queue.get()
        # print(f"{threading.current_thread().name}: after calling get\n, ends=""") -Debugging
        #print(f"{url=}\n", end="")
        if url == "DONE":
            data_queue.put("DONE")
            break

        # TODO process the value retrieved from the queue

        # TODO make Internet call to get characters name and print it out
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            names.append(response["name"])
        else:
            print("RESPONSE = ", response.status_code)

    # TODO - send an alphabetized list of names to the print_names thread
    barrier.wait()
    if thread_index == 0:
        names.sort()
        print_queue.put(names)
        print_queue.put("DONE")

def file_reader(data_queue: Queue): # TODO add arguments
    """ This thread reads the data file and places the values in the data_queue """
    # TODO Open the data file "urls.txt" and place items into a queue
    with open("C:/Users/surplus/Documents/GitHub/maddymcgreer-cse251/week06/team/urls.txt") as f:
        for line in f:
            data_queue.put(line.strip())

    data_queue.put("DONE")
    # TODO signal the retrieve threads one more time that there are "no more values"


def print_names(print_queue: Queue) -> None:
    while True:
        names = print_queue.get()
        print(f"{names=}")
        if names == "DONE":
            break
        
        for name in names:
            print(name, end=", ")

        #assert(len(names) == 38)


def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()
    
    # TODO create queue (if you use the queue module, then you won't need semaphores/locks)
    data_queue = Queue()
    print_queue = Queue()
    threads = []
    names = []

    #create barrier
    barrier = Barrier(RETRIEVE_THREADS)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread needed to do their jobs
    file_reader_thread = Thread(target=file_reader, args=(data_queue,))
     # TODO Get them going
    file_reader_thread.start()
    threads.append(file_reader_thread)

    
    for i in range(RETRIEVE_THREADS):
        t= Thread(target=retrieve_thread, args=(i, data_queue, print_queue, names, barrier))
        t.start()
        threads.append(t)

    print_thread = Thread(target=print_names, args=(print_queue, ))
    print_thread.start()
    threads.append(print_thread)

    # TODO Wait for them to finish
    for t in threads:
        t.join()

    #for _ in range (data_queue.qsize()):
    #    print(f"{data_queue.get()}")

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time to process all URLS = {total_time} sec')


if __name__ == '__main__':
    main()




