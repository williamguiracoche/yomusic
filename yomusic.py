from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Song, User
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "YoMusic"
engine = create_engine('sqlite:///music.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    print login_session['access_token']
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print access_token
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        flash("User not connected.")
        return redirect(url_for('showGenres'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    login_session.clear()
    if result['status'] == '200':
        login_session.clear()
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        login_session['access_token'] = None
        login_session['username'] = None
        login_session.clear()
        flash("Successfully disconnected.")
        return redirect(url_for('showGenres'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        print response
        return response

@app.route('/genres/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(Genres=[genre.serialize for genre in genres])

@app.route('/genre/<int:genre_id>/JSON')
def showPlaylistJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    songs = session.query(Song).filter_by(genre_id = genre_id).all()
    return jsonify(Playlist=[song.serialize for song in songs])

@app.route('/genre/<int:genre_id>/<int:song_id>/JSON')
def showSongJSON(genre_id, song_id):
    song = session.query(Song).filter_by(id = song_id).one()
    return jsonify(Song=song.serialize)

@app.route('/genres')
@app.route('/music')
@app.route('/')
def showGenres():
    genres = session.query(Genre).all()
    if 'username' not in login_session:
        return render_template('publicGenres.html', genres=genres)
    else:
        user_id = login_session['user_id']
        return render_template('genres.html', genres = genres, user_id=user_id)

@app.route('/genre/new', methods=['GET', 'POST'])
def newGenre():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        try:
            newGenre = Genre(name=request.form['name'], user_id=login_session['user_id'])
            session.add(newGenre)
            flash('Created %s' % newGenre.name)
            session.commit()
        except:
            session.rollback()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')

@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
def editGenre(genre_id):
    editedGenre = session.query(Genre).filter_by(id = genre_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedGenre.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit. Please create your own genre in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            session.add(editedGenre)
            session.commit()
            flash('Successfully Edited %s' % editedGenre.name)
            return redirect(url_for('showGenres'))
    else:
        return render_template('editGenre.html', genre = editedGenre)

@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    deletedGenre = session.query(Genre).filter_by(id= genre_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedGenre.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete. Please create your own genre in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(deletedGenre)
        session.commit()
        flash('%s Successfully Deleted' % deletedGenre.name)
        return redirect(url_for('showGenres'))
    else:
        return render_template('deleteGenre.html', genre = deletedGenre)

@app.route('/genre/<int:genre_id>')
@app.route('/genre/<int:genre_id>/playlist')
def showPlaylist(genre_id):
    genre = session.query(Genre).filter_by(id= genre_id).one()
    creator = getUserInfo(genre.user_id)
    songs = session.query(Song).filter_by(genre= genre).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicPlaylist.html', genre= genre, songs= songs, creator=creator)
    else:
        return render_template('playlist.html', genre= genre, songs= songs, creator=creator)

@app.route('/genre/<int:genre_id>/new', methods=['GET', 'POST'])
def newSong(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id= genre_id).one()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add songs to this playlist. Please create your own playlist in order to add songs.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        newSong = Song(name = request.form['name'], \
            artist = request.form['artist'], album = request.form['album'],\
            genre_id = genre_id)
        session.add(newSong)
        session.commit()
        flash('%s Successfully Added' % (newSong.name))
        return redirect(url_for('showPlaylist', genre_id = genre_id))
    else:
        return render_template('newSong.html', genre = genre)

@app.route('/genre/<int:genre_id>/<int:song_id>/edit', methods=['GET', 'POST'])
def editSong(genre_id, song_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id= genre_id).one()
    editedSong = session.query(Song).filter_by(id= song_id).one()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit songs in this playlist. Please create your own playlist in order to edit your songs.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedSong.name = request.form['name']
        if request.form['artist']:
            editedSong.artist = request.form['artist']
        if request.form['album']:
            editedSong.album = request.form['album']
        session.add(editedSong)
        session.commit()
        flash("Song edited.")
        return redirect(url_for('showPlaylist', genre_id = genre_id))
    else:
        return render_template('editSong.html', genre = genre, song= editedSong)

@app.route('/genre/<int:genre_id>/<int:song_id>/delete', methods=['GET', 'POST'])
def deleteSong(genre_id, song_id):
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete songs in this playlist.');}</script><body onload='myFunction()'>"
    genre = session.query(Genre).filter_by(id= genre_id).one()
    deletedSong = session.query(Song).filter_by(id= song_id).one()
    if request.method == 'POST':
        session.delete(deletedSong)
        session.commit()
        flash("Song deleted.")
        return redirect(url_for('showPlaylist', genre_id= genre_id))
    else:
        return render_template('deleteSong.html', genre= genre, song= deletedSong)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
