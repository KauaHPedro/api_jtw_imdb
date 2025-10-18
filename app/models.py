from sqlalchemy import Column, Integer, String, Float, Text
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)       
    poster_link  = Column(Text, nullable=True)                 
    series_title = Column(String(255), index=True)              
    released_year = Column(Integer, nullable=True)       
    certificate  = Column(String(50), nullable=True)      
    runtime      = Column(String(50), nullable=True)            
    genre        = Column(String(255), nullable=True)           
    imdb_rating  = Column(Float, nullable=True)                
    overview     = Column(Text, nullable=True)                
    meta_score   = Column(Integer, nullable=True)            
    director     = Column(String(255), nullable=True)           
    star1        = Column(String(255), nullable=True)           
    star2        = Column(String(255), nullable=True)          
    star3        = Column(String(255), nullable=True)        
    star4        = Column(String(255), nullable=True)         
    no_of_votes  = Column(Integer, nullable=True)            
    gross        = Column(String(50), nullable=True)            