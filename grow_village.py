import sys
import sqlite3

import villagelib

if __name__ == "__main__":

    db_filename = sys.argv[1]

    people = villagelib.load_people(db_filename)
    
    for person in people:
        print(person)


