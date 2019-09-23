DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS relationships;
DROP VIEW IF EXISTS fathers;
DROP VIEW IF EXISTS mothers;

CREATE TABLE people (
    id text NOT NULL UNIQUE,
    name TEXT NOT NULL,
    clan TEXT NOT NULL,
    year_of_birth INTEGER NOT NULL,
    gender TEXT NOT NULL
);


CREATE TABLE relationships (
  person_1_id INTEGER NOT NULL, 
  relationship TEXT NOT NULL,
  person_2_id INTEGER NOT NULL,
  FOREIGN KEY(person_1_id) REFERENCES people(id),
  FOREIGN KEY(person_2_id) REFERENCES people(id),
  UNIQUE(person_1_id, relationship, person_2_id)
);



CREATE VIEW fathers AS
    SELECT name, clan, year_of_birth
    FROM people
    WHERE id IN (
        SELECT DISTINCT(person_1_id)
        FROM relationships
        WHERE relationship = 'father_of'
    );

CREATE VIEW mothers AS
    SELECT name, clan, year_of_birth
    FROM people
    WHERE id IN (
        SELECT DISTINCT(person_1_id)
        FROM relationships
        WHERE relationship = 'mother_of'
    );

