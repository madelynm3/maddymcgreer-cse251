import threading
'''
Requirements:Create a class that extends the 'threading.Thread'
1.  class (see https://stackoverflow.com/questions/15526858/how-to-extend-a-class-in-python). This means that the class IS a thread. 
   Any objects instantiated using this class ARE threads.
2. Instantiate this thread class that computes the sum of all numbers 
   between one and that number (exclusive)

Psuedocode:
1. In your class, write a constructor (in python a constructor is __init__) and allow a number
   to be passed in as a parameter.
2. The constructor should call the parent class's constructor:
   threading.Thread.__init__(self)
3. Create a local sum variable in your constructor.
4. A thread must have a run function, so create a run function that sums from one to the 
   passed in number (inclusive).
5. In the run function, set the sum on self.
6. In main, instantiate your thread class with the a value of 10.
7. Start the thread.
8. Wait for the thread to finish.
9. Assert that thread object's sum attribute is equal to the appropriate value (see main).
10. Repeat steps 7 through 10 using a value of 13.
11. Repeat steps 7 through 10 using a value of 17.

Things to consider:
a. How do you instantiate a class and pass in arguments (see https://realpython.com/lessons/instantiating-classes/)?
b. How do you start a thread object (see this week's reading)?
c. How will you wait until the thread is done (see this week's reading)?
d. How do you get the value an object's attribute (see https://datagy.io/python-print-objects-attributes/)?
'''
######################
# DO NOT USE GLOBALS #
######################

# Create MyThread class which:
# inherits threading.Thread so that threads can be used for concurrent execution. 
# calculates the sum of numbers from 1 to a specified limit (number). 
# includes the run method that performs this calculation, and the instance variables 
# (number and sum) can be accessed after the thread has completed its execution.
class MyThread(threading.Thread):
   # The constructor method. When an instance of the class is cre4ated, this is called.
   def __init__(self, number: int):
        threading.Thread.__init__(self)
        self.number = number
        self.sum = 0

   # Method that is executed once thread is started
   # Calculate sum from 1 to limit     
   def run(self):
       for i in range(1, self.number):
           self.sum += i

def main():
    # Instantiate MyThread class using values 10, 13, and 17
    t10 = MyThread(10)
    t13 = MyThread(13)
    t17 = MyThread(17)
    
   # Store the threads in a list
   # Use 2 for loops to start and join threads
    threads = [t10,t13,t17]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


   # Test (assert) if its sum attribute is equal
    assert t10.sum == 45, f'The sum should equal 45 but instead was {t10.sum}'
    assert t13.sum == 78, f'The sum should equal 78 but instead was {t13.sum}'
    assert t17.sum == 136, f'The sum should equal 136 but instead was {t17.sum}'

if __name__ == '__main__':
    main()
    assert threading.active_count() == 1
    print("DONE")
