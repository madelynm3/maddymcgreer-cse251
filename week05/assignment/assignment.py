'''
Requirements
1. Using two threads, put cars onto a shared queue, with one thread consuming
   the items from the queue and the other producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. Produce a Plot of car count vs queue size (okay to use q.size since this is not a
   condition statement).
   
Questions:
1. Do you need to use locks around accessing the queue object when using multiple threads? 
   Why or why not?
   > Yes, because a queue is usually made to be thread-safe, which
   > means it provides ways to to handle concurrent access from 
   > multiple threads without damaging the data structure/ cause race
   > conditions.
2. How would you define a semaphore in your own words?
   > Semaphores are a type of synchronization primitive. Which means
   > shared and exclusive locks. It is a variable/abtract data type that
   > controls access to a shared resource using multiple threads and
   > avoid problems in a concurrent system.
3. Read https://stackoverflow.com/questions/2407589/what-does-the-term-blocking-mean-in-programming.
   What does it mean that the "join" function is a blocking function? Why do we want to block?
   > The join function is a blocking function because it stops the execution of the calling 
   > thread until the joined thread finishes. We want to use blocking because it is useful for
   > operations where waiting for certain conditions is needed, such as I/O, 
   > thread synchronization, and data management.
   >
'''

from datetime import datetime
import time
import threading
import random
import requests
# DO NOT import queue

from plots import Plots

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

#########################
# NO GLOBAL VARIABLES!
#########################


class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round',
                  'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                  'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

   # Contructor takes 4 parameters: self, queue, car_count, semaphore. 
   # Call constructor of superclass to ensure intitalization
   # Queue paramater assigned to variable to store objects
   # car_count parameter assigned to variable to store the count
    def __init__(self, queue: QueueTwoFiftyOne, semaphore: threading.Semaphore, semaphore_empty: threading.Semaphore, queue_stats, lock):
        super().__init__()
        self.queue = queue
        self.semaphore_empty = semaphore_empty
        self.semaphore = semaphore
        self.stats = queue_stats
        self.lock = lock


   # Iterates through car_count and places the
   # cars in the queue
    def run(self):
        for i in range(self.car_count):
           car = Car()
           with self.lock:
               self.queue.put(car)

           self.semaphore.release()
        
        self.semaphore.acquire()

        self.queue.put(None)

        self.semaphore_empty.release()
        print(">>>>>>>>>>>>>>>>>> MANUFACTURER ENDS")


        # signal the dealer that there there are no more cars


class Dealership(threading.Thread):
    """ This is a dealership that receives cars """

   # Call superclass's instructor and add queue and semaphore attributes
    def __init__(self, queue: QueueTwoFiftyOne, semaphore: threading.Semaphore, semaphore_empty: threading.Semaphore, queue_stats, lock):
        super().__init__()
        self.queue = queue
        self.semaphore_empty = semaphore_empty
        self.semaphore = semaphore
        self.stats = queue_stats
        self.lock = lock

   # Initiates an infinite loop in order to continuously update the queue
   # Acquires semaphore to access queue, checks if empty, get car from
   # queue, release semaphore.
    def run(self):
        while True:
            self.semaphore.acquire()
            with self.lock:
                car = self.queue.get()
                if car == None:
                    break
                self.stats[self.queue.size()] += 1
            
            self.semaphore.release()

            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
        
        print(">>>>>>>>>>>>>>>>>>>> DEALERSHIP ENDS")


def main():
    # random amount of cars to produce
    CARS_TO_PRODUCE = random.randint(500, 600)

    # Create queue (using class QueueTwoFiftyOne)
    queue = QueueTwoFiftyOne()

   # Create semaphores
    semaphore = threading.Semaphore(MAX_QUEUE_SIZE)

    # Block empty queue
    semaphore_empty = threading.Semaphore(0)

    # This tracks the length of the car queue during receiving cars by the dealership,
    # the index of the list is the size of the queue. Update this list each time the
    # dealership receives a car (i.e., increment the integer at the index using the
    # queue size).
    queue_stats = [0] * MAX_QUEUE_SIZE

    # Create lock
    lock = threading.Lock()

   # Create manufacturer and dealership
    factory = Manufacturer(CARS_TO_PRODUCE, queue, semaphore_empty, semaphore, lock)
    dealership = Dealership(queue, semaphore_empty, semaphore, queue_stats, lock)

    # Start manufacturer and dealership threads
    factory.start()
    dealership.start()

    # Wait for manufacturer and dealership to complete
    factory.join()
    dealership.join()


    # Plot car count vs queue size
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats,
             title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')


if __name__ == '__main__':
    main()
