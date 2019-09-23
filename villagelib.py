import sys
import sqlite3
from random import randrange, choice, uniform, seed
import hashlib

from functools import lru_cache

from typing import Type
from dataclasses import dataclass


from sqlalchemy import create_engine



import names





@lru_cache(maxsize=None)
def preg_thr(here_age, n_kids=0, thrs:tuple=(15, 25, 35)):
    
    thr1, thr2, thr3 = thrs
    
    if here_age < thr1:
        prob = 0.0
    elif thr1<= here_age < thr2:
        prob = 0.2
    elif thr2<= here_age < thr3:
        x = (here_age - thr2)/(thr3 - thr2)
        prob = 0.2 - (0.1 * x)
    elif thr3 <= here_age:
        prob = 0.0
        
    return prob * (0.95 ** n_kids)


@dataclass
class Person:
    yob: int
    gender: str = ''
    name: str = ''
    clan: str = ''
    
    def __post_init__(self):
        if not self.gender:
            self.gender = choice(['male', 'female'])
        if not self.name:
            self.name = names.get_first_name(gender=self.gender)
        if not self.clan:
            self.clan = names.get_last_name()
        
        self.kids = []

    @property            
    def id(self):
        return hashlib.md5(repr(self).encode('utf-8')).hexdigest()

@dataclass
class Family:
    husb: Type[Person]
    wife: Type[Person]
    
    def __post_init__(self):
        self.kid_ids = []
        
    @property
    def clan(self):
        return self.husb.clan

    @property
    def number_of_kids(self):
        return len(self.kid_ids)
        
    def extract_relationships(self):                
        yield (self.husb.id, 'married_to', self.wife.id)
        yield (self.wife.id, 'married_to', self.husb.id)
        
        for kid_id in self.kid_ids:
            yield (self.husb.id, 'father_of', kid_id)
            yield (self.wife.id, 'mother_of', kid_id)
            yield (kid_id, 'offspring_of', self.husb.id)
            yield (kid_id, 'offspring_of', self.wife.id)

        
    def baby_this_year(self, year) -> bool:
        
        new_born = None
        
        have_we_got_one =  uniform(0, 1) <  preg_thr(year-self.wife.yob, n_kids=len(self.kid_ids))
        if have_we_got_one is True:
            new_born = Person(year, clan=self.husb.clan)
            self.kid_ids.append(new_born.id)
            
            assert len(self.kid_ids) == len(set(self.kid_ids))

        return new_born


def serialize_people(db_filename, people):
    with sqlite3.connect(db_filename) as conn:
        curs = conn.cursor()
        
        for person in people:
            q = f"INSERT INTO people (id, name, clan, year_of_birth, gender) VALUES ('{person.id}', '{person.name}', '{person.clan}', {person.yob}, '{person.gender}')"
            curs.execute(q)
            
        conn.commit()


def serialize_relationships(db_filename, family):

    with sqlite3.connect(db_filename) as conn:
        curs = conn.cursor()

        for (person1, rel, person2) in family.extract_relationships():
            q = f"INSERT INTO relationships (person_1_id, relationship, person_2_id) VALUES ('{person1}', '{rel}', '{person2}');"
            curs.execute(q)
            
        conn.commit()


def create_family():
    offset = randrange(-10,+10)
    
    husb = Person(gender='male', yob=offset+randrange(10))
    wife = Person(gender='female', yob=offset+randrange(10))

    return Family(husb=husb, wife=wife)

def load_people(db_filename):
    with sqlite3.connect(db_filename) as conn:
        curs = conn.cursor()
        
        curs.execute("SELECT name, clan, year_of_birth, gender FROM people;")
        rows = curs.fetchall()
        
    return [Person(yob=year_of_birth, gender=gender, name=name, clan=clan) for name, clan, year_of_birth, gender in rows]
 
        
        
