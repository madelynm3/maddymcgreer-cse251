'''
Requirements
1. Write a multithreaded program that calls a local web server. The web server is 
   provided to you. It will return data about the Star Wars movies.
2. You will make 94 calls to the web server, using 94 threads to get the data.
3. Using a new thread each time, obtain a list of the characters, planets, 
   starships, vehicles, and species of the sixth Star Wars movie.
3. Use the provided print_film_details function to print out the data 
   (you can modify it if you need).
   
Questions:
1. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
    > This assignment is IO Bound. API calls are usually IO operations becasue the program waits to respond to the server with the data. Since this assignment is waiting heavily on responses from the server, this would be primarily an IO bound problem.
2. Review dictionaries (see https://isaaccomputerscience.org/concepts/dsa_datastruct_dictionary). How could a dictionary be used on this assignment to improve performance?
    > Dictionaries can help performance by accessing and organizing data retrieved by API calls. It uses storage so that the 94 API calls in the 94 threads can run concurrently. I used a dictionary called category_results. 
'''


from datetime import datetime, timedelta
import time
import requests
import json
import threading


# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

# This class is used in a multithreaded program where 
# multiple instances of this class can run concurrently to make 
# API calls and store the results in a result list. 
# The lock ensures that the shared result list is accessed 
# safely by multiple threads.
class APICallThread(threading.Thread):
    def __init__(self, url, category, result_list, lock):
        threading.Thread.__init__(self)
        self.url = url
        self.category = category
        self.result_list = result_list
        self.lock = lock
    
    def run(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in thread {self.category}: {e}")
            data = {}




def print_film_details(films, chars, planets, starships, vehicles, species):
    '''
    Print out the film details in a formatted way
    '''
    
    def display_names(title, name_list):
        print('')
        print(f'{title}: {len(name_list)}')
        names = sorted([item["name"] for item in name_list])
        print(str(names)[1:-1].replace("'", ""))

    print('-' * 40)
    print(f'Title   : {films["title"]}')
    print(f'Director: {films["director"]}')
    print(f'Producer: {films["producer"]}')
    print(f'Released: {films["release_date"]}')

    display_names('Characters', chars)
    display_names('Planets', planets)
    display_names('Starships', starships)
    display_names('Vehicles', vehicles)
    display_names('Species', species)


def main():
    #Start a timer
    begin_time = time.perf_counter()
    
    print('Starting to retrieve data from the server')

    # This creates parallel execution of API calls 
    # for different categories using multiple threads. 
    # The use of a lock ensures that the shared category_results 
    # dictionary is updated by multiple threads.
    
    # Add a lock for synchronization
    thread_lock = threading.Lock()

    # List of categories to retrieve
    categories = ['people', 'planets', 'starships', 'vehicles', 'species']

    # Dictionary to store each category's results
    category_results = {}

    # Create threads for each category
    threads = [APICallThread(f'{TOP_API_URL}/{category}/', category, category_results, thread_lock) for category in categories]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Print the results for each category
    for category in categories:
        print(f'{category} result: {category_results.get(category, {})}')

    # film_result dictionary collects the 
    # details about the sixth film.
    film_url = f'{TOP_API_URL}/films/6'
    film_result = {}
    film_thread = APICallThread(film_url, 'films', film_result, thread_lock)
    film_thread.start()
    film_thread.join()

    # Print the result for film 6
    print(f'Film 6 result: {film_result.get("films", {})}')
    
    # This function obtains the data for displaying
    # film details using the print_film_details function.
    def extract_film_data(category_results):
      # Get data for each category
      film_data = category_results.get('films', {})
      people_data = category_results.get('people', [])
      chars = people_data[0].get('characters', []) if people_data else []
      planets = film_data.get('planets', [])
      starships = film_data.get('starships', [])
      vehicles = film_data.get('vehicles', [])
      species = film_data.get('species', [])

      return film_data, chars, planets, starships, vehicles, species

    # Call the display function
    film_data, chars, planets, starships, vehicles, species = extract_film_data(category_results)
    print_film_details(film_data, chars, planets, starships, vehicles, species)

    print(f'There were {call_count} calls to the server')
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f'Total time = {total_time_str} sec')
    
    # If you do have a slow computer, then put a comment in your code about why you are changing
    # the total_time limit. Note: 90+ seconds means that you are not doing multithreading
    assert total_time < 15, "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."
    
    assert call_count == 94, "It should take exactly 94 threads to get all the data"
    

if __name__ == "__main__":
    main()
