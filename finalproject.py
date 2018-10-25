from flask import Flask, render_template

app = Flask(__name__)

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
    return "This page will show all my genres"
    #return render_template('genres.html', genres = genres)

@app.route('/genre/new')
def newGenre():
    return "This page will be for making a new genre"
    #return render_template('newGenre.html')

@app.route('/genre/<int:genre_id>/edit')
def editGenre(genre_id):
    return "This page will be for editing genre %s" %genre_id
    #return render_template('editGenre.html', genre = genre)

@app.route('/genre/<int:genre_id>/delete')
def deleteGenre(genre_id):
    return "This page will be for deleting genre %s" %genre_id
    #return render_template('deleteGenre.html', genre = genre)

@app.route('/genre/<int:genre_id>')
@app.route('/genre/<int:genre_id>/playlist')
def showPlaylist(genre_id):
    return "This page is the playlist for genre %s" %genre_id
    #return render_template('playlist.html',genre = genre, songs = songs)

@app.route('/genre/<int:genre_id>/new')
def newSong(genre_id):
    return "This page is for making a new song for genre %s" %genre_id
    #return render_template('newPlaylist.html', genre = genre)

@app.route('/genre/<int:genre_id>/<int:song_id>/edit')
def editSong(genre_id, song_id):
    return "This page is for editing song %s for genre %s" %(song_id, genre_id)
    #return render_template('editPlaylist.html', genre = genre, song= song)

@app.route('/genre/<int:genre_id>/<int:song_id>/delete')
def deleteSong(genre_id, song_id):
    return "This page is for deleting playlist song %s for genre %s" %(song_id, genre_id)
    #return render_template('deletePlaylist.html', genre= genre, song= song)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
