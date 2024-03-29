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
    def __init__(self, url) -> None:
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}
    
    def run(self) -> None:
        global call_count
        http_response = requests.get(self.url)
        call_count += 1
        if http_response.status_code == 200:
            self.response = http_response.json()

def print_film_details(urls) -> list[Any]:
    results = []
    threads = []
    
    for url in urls:
        t = Request_thread(url)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        results.append(t.response)
    
    return results
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


def fetch_category_data(category_urls, lock):
    '''
    Function to fetch data for each category using multiple threads
    '''
    response_list = []
    threads = []
    
    # Create threads for each URL in the category_urls list
    for url in category_urls:
        thread = APICallThread(url, url.split('/')[-2], response_list, lock)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    return response_list


def main():
    # Start a timer
    begin_time = time.perf_counter()
    
    print('Starting to retrieve data from the server')

    # Add a lock for synchronization
    thread_lock = threading.Lock()

    # Fetching URLs for film 6 and its details
    t = APICallThread(TOP_API_URL, 'top_urls', {}, thread_lock)
    t.start()
    t.join()
    top_urls = t.result_list

    film_url = top_urls['films']
    t = APICallThread(f'http://127.0.0.1:8790/films/6/', 'film_data', {}, thread_lock)
    t.start()
    t.join()
    film_data = t.result_list

    # Extract URLs for different categories
    char_urls = film_data['characters']
    planet_urls = film_data['planets']
    starship_urls = film_data['starships']
    vehicle_urls = film_data['vehicles']
    species_urls = film_data['species']

    # Fetch data for each category
    category_urls = [char_urls, planet_urls, starship_urls, vehicle_urls, species_urls]
    category_results = fetch_category_data(category_urls, thread_lock)

    # Print the results for each category
    for category, result in category_results.items():
        print(f'{category} result: {result}')

    # Display film details
    print_film_details(film_data, category_results['characters'], category_results['planets'], 
                       category_results['starships'], category_results['vehicles'], 
                       category_results['species'])

    # Print statistics
    print(f'There were {call_count} calls to the server')
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f'Total time = {total_time_str} sec')
    

    assert total_time < 15, "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."
    assert call_count == 94, "It should take exactly 94 threads to get all the data"


if __name__ == "__main__":
    main()
