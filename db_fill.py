from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Genre, Song

engine = create_engine('sqlite:///music.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Playlist for Rock
genre0 = Genre(name="Rock")
session.add(genre0)
session.commit()

song0 = Song(name="Mr. Brightside", artist="The Killers", album="Hot Fuss", genre=genre0)
session.add(song0)
session.commit()

song1 = Song(name="Seven Nation Army", artist="The White Stripes", album="Elephant", genre=genre0)
session.add(song1)
session.commit()

song2 = Song(name="Uprising", artist="Muse", album="The Resistance", genre=genre0)
session.add(song2)
session.commit()

song3 = Song(name="Do I Wanna Know?", artist="Arctic Monkeys", album="AM", genre=genre0)
session.add(song3)
session.commit()

song4 = Song(name="Welcome to the Black Parade", artist="My Chemical Romance", album="The Black Parade", genre=genre0)
session.add(song4)
session.commit()


#Playlist for Hip Hop
genre1 = Genre(name="Hip Hop")
session.add(genre1)
session.commit()

song0 = Song(name="Poetic Justice", artist="Kendrick Lamar", album="good kid, m.A.A.d. City", genre=genre1)
session.add(song0)
session.commit()


song1 = Song(name="No Role Modelz", artist="J. Cole", album="2014 Forest Hills Drive", genre=genre1)
session.add(song1)
session.commit()

song2 = Song(name="No Problem", artist="Chance the Rapper", album="Coloring Book", genre=genre1)
session.add(song2)
session.commit()

song3 = Song(name="Empire State of Mind", artist="Jay-Z", album="The Blueprint 3", genre=genre1)
session.add(song3)
session.commit()

song4 = Song(name="Sanctified", artist="Rick Ross", album="Mastermind", genre=genre1)
session.add(song4)
session.commit()

#Playlist for Electronic
genre2 = Genre(name="Electronic")
session.add(genre2)
session.commit()

song0 = Song(name="Adagio for Strings", artist="Tiesto", album="Just Be", genre=genre2)
session.add(song0)
session.commit()

song1 = Song(name="Clarity", artist="Zedd", album="Clarity", genre=genre2)
session.add(song1)
session.commit()

song2 = Song(name="Titanium", artist="David Guetta", album="Nothing but the Beat", genre=genre2)
session.add(song2)
session.commit()

song3 = Song(name="Don't You Worry Child", artist="Swedish House Mafia", album="Until Now", genre=genre2)
session.add(song3)
session.commit()

song4 = Song(name="Wake Me Up", artist="Avicii", album="True", genre=genre2)
session.add(song4)
session.commit()

print "added songs!"
