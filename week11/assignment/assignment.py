'''
Purpose: Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        ***************************************************
        ** DO NOT search for a solution on the Internet, **
        ** your goal is not to copy a solution, but to   **
        ** work out this problem.                        **
        ***************************************************

- When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be an issue picking up the two forks since the waiter is in control of 
  the forks. When a philosopher is finished eating, it will inform the waiter that they
  are finished.  If the waiter indicates to a philosopher that they can not eat, the 
  philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout. This can be useful to not
  block when trying to acquire a lock.
- Philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- Philosophers need to think (digest?) for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks (minimum of 5 philosophers).
- Use threads for this problem.
- Provide a way to "prove" that each philosophers will not starve. This can be counting
  how many times each philosophers eat and display a summary at the end. Or, keeping track
  how long each philosopher is eating and thinking.
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat. Hint, they are
  sitting in a circle.
'''

import time
import threading

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5

class Waiter:
    def __init__(self):
        self.forks = [threading.Lock() for _ in range(PHILOSOPHERS)]
        self.available = threading.Semaphore(PHILOSOPHERS - 1)

    def request_to_eat(self, philosopher_id):
        if self.available.acquire(timeout=1):
            self.forks[philosopher_id].acquire()
            self.forks[(philosopher_id + 1) % PHILOSOPHERS].acquire()
            return True
        return False

    def finished_eating(self, philosopher_id):
        self.forks[philosopher_id].release()
        self.forks[(philosopher_id + 1) % PHILOSOPHERS].release()
        self.available.release()

def philosopher_behavior(name, waiter):
    """
    Simulates philospher behavior and interactions
    between philospher and waiter.
    
    Parameters:
        name (str): Philosopher name
        waiter (Waiter): Waiter controlling access to forks
    """
    meals_eaten = 0
    while meals_eaten < MAX_MEALS:
        philosopher_id = name.index(name)
        if waiter.request_to_eat(philosopher_id):
            print(f"{name} is eating.")
            time.sleep(1 + philosopher_id % 3)  # Eating delay
            waiter.finished_eating(philosopher_id)
            meals_eaten += 1
        else:
            print(f"{name} is waiting.")
            time.sleep(1 + philosopher_id % 3)  # Waiting delay
    print(f"{name} finished eating {MAX_MEALS} meals.")

def main():
    """
    Main function to demonstrate philosopher simulation.
    """
    waiter = Waiter()
    philosopher_names = ["Hegel", "Sartre", "Nietzsche", "Camus", "Plato"]  # Names of philosophers because I think it's funny
    philosophers = []
    for name in philosopher_names:
        philosopher = threading.Thread(target=philosopher_behavior, args=(name, waiter))
        philosopher.start()
        philosophers.append(philosopher)

    for philosopher in philosophers:
        philosopher.join()

if __name__ == '__main__':
    main()
