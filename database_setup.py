import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    
class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Song(Base):
    __tablename__ = 'song'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    artist = Column(String(80))
    album = Column(String(80))
    video_url = Column(String(250))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'album': self.album
        }

engine = create_engine('sqlite:///music.db')


Base.metadata.create_all(engine)
