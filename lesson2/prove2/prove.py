"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Cole Williams

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_Thread(threading.Thread):
  def __init__(self, url, list):
      # Call the Thread class's init function
      # threading.Thread.__init__(self)
      super().__init__()
      self.url = url
      self.response = {}
      self.status_code = {}
      self.list = list

  def run(self):
      global call_count
      call_count+=1
      response = requests.get(self.url)
      # Check the status code to see if the request succeeded.
      self.status_code = response.status_code
      if response.status_code == 200:
          self.response = response.json()
          self.list.append(self.response['name'])
      else:
          print('RESPONSE = ', response.status_code)

# TODO Add any functions you need here


def main():
    threads = []
    characters = []
    planets = []
    starships = []
    vehicles = []
    species = []
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    response = requests.get(TOP_API_URL)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        # print(f'\nHere is the URL for person id = 1 {TOP_API_URL}/people/1')
    # TODO Retrieve Details on film 6
    film = requests.get(f'{TOP_API_URL}/films/6')
    if film.status_code == 200:
        filmdata = film.json()
        # for i in filmdata:
        #     print(i)
            #print(data[i])

    #print(filmdata['characters'])
    for i in filmdata['characters']:
        char = Request_Thread(rf'{i}', characters)
        threads.append(char)

    for i in filmdata['planets']:
        char = Request_Thread(rf'{i}', planets)
        threads.append(char)

    for i in filmdata['starships']:
        char = Request_Thread(rf'{i}', starships)
        threads.append(char)

    for i in filmdata['vehicles']:
        char = Request_Thread(rf'{i}', vehicles)
        threads.append(char)

    for i in filmdata['species']:
        char = Request_Thread(rf'{i}', species)
        threads.append(char)


    for i in threads:
        i.start()
    for i in threads:
        i.join()

    # TODO Display results
    print("-"*50)
    print("{:_<20}".format(f"Title: {filmdata['title']}"))
    print("{:_<20}".format(f"Director: {filmdata['director']}"))
    print("{:_<20}".format(f"Producer: {filmdata['producer']}"))
    print("{:_<20}".format(f"Released: {filmdata['release_date']}"))
    print()
    print(f"Characters: {len(characters)}")
    print(", ".join(sorted(characters)))
    print()
    print(f"Planets: {len(planets)}")
    print(", ".join(sorted(planets)))
    print()
    print(f"Starships: {len(starships)}")
    print(", ".join(sorted(starships)))
    print()
    print(f"Vehicles: {len(vehicles)}")
    print(", ".join(sorted(vehicles)))
    print()
    print(f"Species: {len(species)}")
    print(", ".join(sorted(species)))
    print()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()