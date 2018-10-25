from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Song

app = Flask(__name__)

engine = create_engine('sqlite:///music.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Sample Genres
genre = {'name': 'Rock', 'id': '1'}

genres = [{'name': 'Rock', 'id': '1'}, {'name':'Hip Hop', 'id':'2'},{'name':'Electronic', 'id':'3'}]


#Sample Playlists
songs = [ {'name':'Mr. Brightside', 'artist':'The Killers', 'album':'Hot Fuss', 'id':'1'}, {'name':'Seven Nation Army','artist':'The White Stripes', 'album':'Elephant','id':'2'},{'name':'Uprising','artist':'Muse', 'album':'The Resistance','id':'3'},{'name':'Do I Wanna Know?','artist':'Arctic Monkeys', 'album':'AM','id':'4'},{'name':'Welcome to the Black Parade','artist':'My Chemical Romance', 'album':'The Black Parade','id':'5'} ]
song =  {'name':'Mr. Brightside', 'artist':'The Killers', 'album':'Hot Fuss'}

@app.route('/')
@app.route('/music')
@app.route('/genres')
def showGenres():
    genres = session.query(Genre).all()
    return render_template('genres.html', genres = genres)

@app.route('/genre/new', methods=['GET', 'POST'])
def newGenre():
    if request.method == 'POST':
        newGenre = Genre(name=request.form['name'])
        session.add(newGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')

@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
def editGenre(genre_id):
    editedGenre = session.query(Genre).filter_by(id = genre_id).one()
    if request.method == 'POST':
        editedGenre.name = request.form['name']
        session.add(editedGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('editGenre.html', genre = editedGenre)

@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    deletedGenre = session.query(Genre).filter_by(id= genre_id).one()
    if request.method == 'POST':
        session.delete(deletedGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('deleteGenre.html', genre = deletedGenre)

@app.route('/genre/<int:genre_id>')
@app.route('/genre/<int:genre_id>/playlist')
def showPlaylist(genre_id):
    #return "This page is the playlist for genre %s" %genre_id
    return render_template('playlist.html',genre = genre, songs = songs)

@app.route('/genre/<int:genre_id>/new')
def newSong(genre_id):
    #return "This page is for making a new song for genre %s" %genre_id
    return render_template('newSong.html', genre = genre)

@app.route('/genre/<int:genre_id>/<int:song_id>/edit')
def editSong(genre_id, song_id):
    #return "This page is for editing song %s for genre %s" %(song_id, genre_id)
    return render_template('editSong.html', genre = genre, song= song)

@app.route('/genre/<int:genre_id>/<int:song_id>/delete')
def deleteSong(genre_id, song_id):
    #return "This page is for deleting playlist song %s for genre %s" %(song_id, genre_id)
    return render_template('deleteSong.html', genre= genre, song= song)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
