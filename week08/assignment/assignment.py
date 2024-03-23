'''
Requirements
1. Create a multiprocessing program that connects the processes using Pipes.
2. Create a process from each of the following custom process classes, 
   Marble_Creator, Bagger, Assembler, and Wrapper.
3. The Marble_Creator process will send a marble to the Bagger process using
   a Pipe.
4. The Bagger process will create a Bag object with the required number of
   marbles. 
5. The Bagger process will send the Bag object to the Assembler using a Pipe.
6. The Assembler process will create a Gift object and send it to the Wrapper
   process using a Pipe.
7. The Wrapper process will write to a file the current time followed by the 
   gift string.
8. The program should not hard-code the number of marbles, the various delays,
   nor the bag count. These should be obtained from the settings.txt file.
   
Questions:
1. Why can you not use the same pipe object for all the processes (i.e., why 
   do you need to create three different pipes)?
   > It is necessary to use separate pipes for each pair of communicating processes because pipes are unidirectional and blocking in python.
   > Separate pipes for communicating  process pairs allows scalaility, isolation, and improved maintenance.
   > Using the same pipe would introduce complexities, deadlocks, and communication difficulty between processes.

   2. Compare and contrast pipes with queues (i.e., how are the similar or different)?
   > Compare: Both are used for inter-process communication
   > Contract: Pipes are unidirectional while queues are bidirectional.
   > Pipes are default blocking, queues can be blocking or non-blocking.
   > Pipes transfer strings/raw bytes, queues handle abritrary objects.
   > Queues are automatically synchronized, while pipes have to be managed manually.
'''

import datetime
import json
import multiprocessing as mp
import os
import random
import time

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables


class Bag():
    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, bagger_conn, marble_count, creator_delay):
        mp.Process.__init__(self)
        self.bagger_conn = bagger_conn
        self.marble_count = marble_count
        self.creator_delay = creator_delay

    def run(self):
        for _ in range(self.marble_count):
            marble = random.choice(self.colors)
            self.bagger_conn.send(marble)
            time.sleep(self.creator_delay)
        self.bagger_conn.close()

        


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self, assembler_conn, bag_count, bagger_delay):
        mp.Process.__init__(self)
        self.assembler_conn = assembler_conn
        self.bag_count = bag_count
        self.bagger_delay = bagger_delay

    def run(self):
        bags = []
        while True:
            marble = self.assembler_conn.recv()
            if marble is None:
                break
            bags.append(marble)
            if len(bags) == self.bag_count:
                self.assembler_conn.send(bags)
                bags = []
            time.sleep(self.bagger_delay)


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, wrapper_conn, assembler_delay):
        mp.Process.__init__(self)
        self.wrapper_conn = wrapper_conn
        self.assembler_delay = assembler_delay

    def run(self):
        bag = self.wrapper_conn.recv()
        while bag is not None:
            #bag = self.wrapper_conn.recv()
            #if bag is None:
                #break
            large_marble = random.choice(self.marble_names)
            gift = Gift(large_marble, bag)
            self.wrapper_conn.send(gift)
            time.sleep(self.assembler_delay)




class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """

    def __init__(self, wrapper_conn, boxes_filename=BOXES_FILENAME, wrapper_delay=WRAPPER_DELAY):
        mp.Process.__init__(self)
        self.wrapper_conn = wrapper_conn
        self.boxes_filename = boxes_filename
        self.wrapper_delay = wrapper_delay

    def run(self):
        try:
            with open(self.boxes_filename, 'a') as boxes_file:
                while True:
                    gift = self.wrapper_conn.recv()
                    if gift is None:
                        break
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    boxes_file.write(f'{timestamp}: {gift}\n')
                    boxes_file.flush()  # Flush buffer to ensure immediate write
                    time.sleep(self.wrapper_delay)

        except Exception as e:
            print(f"Error in Wrapper process: {e}")


def display_final_boxes(filename):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        print(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                print(line.strip())
    else:
        print(
            f'ERROR: The file {filename} doesn\'t exist.  No boxes were created.')


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        print(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    print(f'Marble count                = {settings[MARBLE_COUNT]}')
    print(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    print(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    print(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    print(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    print(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # Pipes between creator -> bagger -> assembler -> wrapper
    creator_to_bagger_conn, bagger_to_creator_conn = mp.Pipe()
    bagger_to_assembler_conn, assembler_to_bagger_conn = mp.Pipe()
    assembler_to_wrapper_conn, wrapper_to_assembler_conn = mp.Pipe()


    # Count the number of gifts
    gift_count = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    print('Create the processes')

    # Create the processes (ie., classes above)
    processes = [
        Marble_Creator(bagger_to_creator_conn, settings[MARBLE_COUNT], settings[CREATOR_DELAY]),
        Bagger(assembler_to_bagger_conn, settings[BAG_COUNT], settings[BAGGER_DELAY]),
        Assembler(wrapper_to_assembler_conn, settings[ASSEMBLER_DELAY]),
        Wrapper(wrapper_to_assembler_conn, BOXES_FILENAME, settings[WRAPPER_DELAY])
    ]


    print('Starting the processes')
    # Start processes
    for process in processes:
        process.start()


    print('Waiting for processes to finish')
    # Join processes
    for process in processes:
        process.join()

    # Close pipes
    creator_to_bagger_conn.close()
    bagger_to_creator_conn.close()
    bagger_to_assembler_conn.close()
    assembler_to_bagger_conn.close()
    assembler_to_wrapper_conn.close()
    wrapper_to_assembler_conn.close()

    display_final_boxes(BOXES_FILENAME)

    # Print the number of gifts created.
    print(f'Number of gifts created: {gift_count.value}')
    
    # End timer
    end_time = time.perf_counter()
    elapsed_time = end_time - begin_time
    print(f"Elapsed time: {elapsed_time} seconds")


if __name__ == '__main__':
    main()
