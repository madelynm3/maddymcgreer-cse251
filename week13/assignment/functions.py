"""
Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04

Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')

10% Bonus to speed up part 3
"""
import threading
from common import *

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # Implement Depth first retrieval
    def dfs(family_id, tree):
        req = Request_thread(f'{TOP_API_URL}/family/{family_id}')
        req.start()
        req.join()
        family_data = req.response
        family_data = req.response.json()

        # Family object created and added to tree
        family = Family(family_id, family_data)
        tree.add_family(family)

        husband_id = family_data['husband_id']
        wife_id = family_data['wife_id']
        if husband_id:
            req = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
            req.start()
            req.join()
            husband_data = req.response
            husband = Person(husband_data)
            tree.add_person(husband)
        
        if wife_id:
            req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
            req.start()
            req.join()
            wife_data = req.response
            wife = Person(wife_data)
            tree.add_person(wife)
        
        for child_id in family_data['children']:
            dfs(child_id, tree)
    
    dfs(family_id, tree)

    #print('WARNING: DFS function not written')


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    # Implement breadth first retrieval
    # Queue storage for family IDs
    queue = [start_id]

    while queue:
        family_id = queue.pop(0)
    
    req = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req.start()
    req.join()
    family_data = req.response

    family = Family(family_id, family_data)
    tree.add_family(family)

    husband_id = family_data['husband_id']
    wife_id = family_data['wife_id']
    if husband_id:
        req = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
        req.start()
        req.join()
        husband_data = req.response
        husband = Person(husband_data)
        tree.add_person(husband)
    if wife_id:
        req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
        req.start()
        req.join()
        wife_data = req.response
        wife = Person(wife_data)
        tree.add_person(wife)

    # Add children to the queue
    for child_id in family_data['children']:
        queue.append(child_id)

    #print('WARNING: BFS function not written')




# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # - implement breadth first retrieval
    # - Limit number of concurrent connections to the FS server to 5

    queue = [start_id]

    semaphore = threading.Semaphore(5)

    while queue:
        family_id = queue.pop(0)
        semaphore.acquire()

        def process_family():
            req = Request_thread(f'{TOP_API_URL}/family/{family_id}')
            req.start()
            req.join()
            family_data = req.response

            family = Family(family_id, family_data)
            tree.add_family(family)

            husband_id = family_data['husband_id']
            wife_id = family_data['wife_id']
            if husband_id:
                req = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
                req.start()
                req.join()
                husband_data = req.response
                husband = Person(husband_data)
                tree.add_person(husband)
            if wife_id:
                req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
                req.start()
                req.join()
                wife_data = req.response
                wife = Person(wife_data)
                tree.add_person(wife)

            semaphore.release()

            # Add children to the queue
            for child_id in family_data['children']:
                queue.append(child_id)

        # Thread to process the family information
        threading.Thread(target=process_family).start()

    #print('WARNING: BFS (Limit of 5 threads) function not written')

    
