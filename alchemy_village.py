import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class People(Base):
    __tablename__ = 'people'
    
    _id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    clan = Column(String, nullable=False)
    year_of_birth = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    


if __name__ == "__main__":

    db_filename = sys.argv[1]
    db_path = Path(db_filename).resolve()
        
    engine = create_engine(f"sqlite://{db_path}")

    session = sessionmaker(bind=engine)()
    
    person = 
    

