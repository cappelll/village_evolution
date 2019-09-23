import sys
import sqlite3

import villagelib

if __name__ == "__main__":

    people = {}
    db_filename = sys.argv[1]


    for _ in range(10):
        family = villagelib.create_family()
        
        _people = []
        
        print(f"The {family.clan}s created")
        print(family)


        _people.append(family.husb)
        _people.append(family.wife)


        for y in range(10,50):
            new_born = family.baby_this_year(y)
            if new_born is not None:
                _people.append(new_born)

        print(f"The {family.clan}s have now {family.number_of_kids} kids: {family.kid_ids}")

        villagelib.serialize_people(db_filename, _people)
        villagelib.serialize_relationships(db_filename, family)

