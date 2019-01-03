from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Genre, Song, User

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

user1 = User(id=1, name="will", email="will.email.com")

#Playlist for Rock
genre1 = Genre(name="Rock", user=user1)
session.add(genre1)
session.commit()

song1 = Song(name="Mr. Brightside", artist="The Killers", album="Hot Fuss", genre=genre1, user=user1)
session.add(song1)
session.commit()

song2 = Song(name="Seven Nation Army", artist="The White Stripes", album="Elephant", genre=genre1, user=user1)
session.add(song2)
session.commit()

song3 = Song(name="Uprising", artist="Muse", album="The Resistance", genre=genre1, user=user1)
session.add(song3)
session.commit()

song4 = Song(name="Do I Wanna Know?", artist="Arctic Monkeys", album="AM", genre=genre1, user=user1)
session.add(song4)
session.commit()

song5 = Song(name="Welcome to the Black Parade", artist="My Chemical Romance", album="The Black Parade", genre=genre1, user=user1)
session.add(song5)
session.commit()


#Playlist for Hip Hop
genre2 = Genre(name="Hip Hop", user=user1)
session.add(genre2)
session.commit()

song6 = Song(name="Poetic Justice", artist="Kendrick Lamar", album="good kid, m.A.A.d. City", genre=genre2, user=user1)
session.add(song6)
session.commit()


song7 = Song(name="No Role Modelz", artist="J. Cole", album="2014 Forest Hills Drive", genre=genre2, user=user1)
session.add(song7)
session.commit()

song8 = Song(name="No Problem", artist="Chance the Rapper", album="Coloring Book", genre=genre2, user=user1)
session.add(song8)
session.commit()

song9 = Song(name="Empire State of Mind", artist="Jay-Z", album="The Blueprint 3", genre=genre2, user=user1)
session.add(song9)
session.commit()

song10 = Song(name="Sanctified", artist="Rick Ross", album="Mastermind", genre=genre2, user=user1)
session.add(song10)
session.commit()

#Playlist for Electronic
genre3 = Genre(name="Electronic", user=user1)
session.add(genre3)
session.commit()

song11 = Song(name="Adagio for Strings", artist="Tiesto", album="Just Be", genre=genre3, user=user1)
session.add(song11)
session.commit()

song12 = Song(name="Clarity", artist="Zedd", album="Clarity", genre=genre3, user=user1)
session.add(song12)
session.commit()

song13 = Song(name="Titanium", artist="David Guetta", album="Nothing but the Beat", genre=genre3, user=user1)
session.add(song13)
session.commit()

song14 = Song(name="Don't You Worry Child", artist="Swedish House Mafia", album="Until Now", genre=genre3, user=user1)
session.add(song14)
session.commit()

song15 = Song(name="Wake Me Up", artist="Avicii", album="True", genre=genre3, user=user1)
session.add(song15)
session.commit()

print "added songs!"
