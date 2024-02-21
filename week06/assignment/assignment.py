'''
Requirements
1. Using multiple threads, put cars onto a shared queue, with one or more thread consuming
   the items from the queue and one or more thread producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. The number of cars produced by the manufacturer must equal the number of cars bought by the 
   dealership. Use necessary data objects (e.g., lists) to prove this. There is an assert in 
   main that must be used.
   
Questions:
1. How would you define a barrier in your own words?
   > A barrier is a synchronization primitive that allows multiple 
   > threads to wait at a certain point until all threads have reached 
   > that point. Once all threads have reached the barrier, 
   > they can proceed with their execution.
   >
2. Why is a barrier necessary in this assignment?
   > A barrier is necessary in this assignment to ensure that all manufacturers 
   > finish producing cars before dealerships start selling them. Without a barrier, 
   > there's a possibility that some dealerships may start selling cars before 
   > all manufacturers have finished producing them, leading to incorrect 
   > statistics or race conditions.
   >
'''

from datetime import datetime, timedelta
import time
import threading
import random

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!


class Car():
    """ This is the Car class that will be created by the manufacturers """

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

        # Display the car that has was just created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, semaphore, barrier, manufacturer_id, manufacturer_stats, cars_to_produce):
        super().__init__() 
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        self.car_queue = car_queue
        self.semaphore = semaphore
        self.barrier = barrier
        self.manufacturer_id = manufacturer_id
        self.manufacturer_stats = manufacturer_stats
        self.cars_to_produce = cars_to_produce

    def run(self):
        for _ in range(self.cars_to_produce):
            self.semaphore.acquire()
            car = Car()
            self.car_queue.put(car)
            self.manufacturer_stats[self.manufacturer_id] += 1
            self.semaphore.release()

        self.barrier.wait()

        if self.manufacturer_id == 0:
            for _ in range(MAX_QUEUE_SIZE):
                self.semaphore.acquire()
                self.car_queue.put(None)  # Signal end of production
                self.semaphore.release()


class Dealership(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue, semaphore, dealer_id, dealer_stats):
        super().__init__()
        self.car_queue = car_queue
        self.semaphore = semaphore
        self.dealer_id = dealer_id
        self.dealer_stats = dealer_stats

    def run(self):
        while True:
            with self.semaphore:  # Acquire the semaphore using a with statement
                car = self.car_queue.get()
            

                if car is None:
                    break
                self.semaphore.release()
                self.dealer_stats[self.dealer_id] += 1

            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def run_production(manufacturer_count, dealer_count):
    # Start a timer
    CARS_TO_PRODUCE = random.randint(500, 600)
    begin_time = time.perf_counter()
    car_queue = QueueTwoFiftyOne()
    semaphore = threading.Semaphore(MAX_QUEUE_SIZE)
    barrier = threading.Barrier(manufacturer_count)
    dealer_stats = [0] * dealer_count
    manufacturer_stats = [0] * manufacturer_count

    manufacturers = [Manufacturer(car_queue, semaphore, barrier, i, manufacturer_stats, CARS_TO_PRODUCE) for i in range(manufacturer_count)]
    dealerships = [Dealership(car_queue, semaphore, i, dealer_stats) for i in range(dealer_count)]

    for dealership in dealerships:
        dealership.start()

    for manufacturer in manufacturers:
        manufacturer.start()

    for manufacturer in manufacturers:
        manufacturer.join()

    for dealership in dealerships:
        dealership.join()

    run_time = time.perf_counter() - begin_time
    return (run_time, car_queue.get_max_size(), dealer_stats, manufacturer_stats)



def main():
    """ Main function """

    # Use 1, 1 to get your code working like the previous assignment, then
    # try adding in different run amounts. You should be able to run the
    # full 7 run amounts.
    #runs = [(1, 1)]
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for manufacturers, dealerships in runs:
        run_time, max_queue_size, dealer_stats, manufacturer_stats = run_production(
            manufacturers, dealerships)

        print(f'Manufacturers       : {manufacturers}')
        print(f'Dealerships         : {dealerships}')
        print(f'Run Time            : {run_time:.2f} sec')
        print(f'Max queue size      : {max_queue_size}')
        print(f'Manufacturer Stats  : {manufacturer_stats}')
        print(f'Dealer Stats        : {dealer_stats}')
        print('')

        # The number of cars produces needs to match the cars sold (this should pass)
        assert sum(dealer_stats) == sum(manufacturer_stats)


if __name__ == '__main__':
    main()
