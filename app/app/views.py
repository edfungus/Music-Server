from flask import render_template, jsonify, request
from app import app, queue
from .musicControl import *

@app.route('/nowPlaying')					
@app.route('/')
def home():
	display = {
			'id': '0001',
			'artwork': '/static/images/home.jpg',
			'title': 'song title',
			'artist': 'artist',
			'album': 'album'
	}
	return render_template('home.html',title='home',display=display)

@app.route('/music')						
def music():
	results = musicSearchResults(True,'')
	return render_template('music.html',title='music',songs=results['titles'])

@app.route('/music/search', methods=['POST'])
def musicSearch():
	query = request.form['query']
	results = musicSearchResults(False,query)
	return jsonify(**results)

@app.route('/music/search/<artist>')
def musicSearchArtist(artist):
	results = getArtist(artist)
	return render_template('music.html',title=results['artistName'],songs=results['titles'],albumCovers=results['albums'],searchBoxText=results['artistName'])

@app.route('/music/search/<artist>/<album>')
def musicSearchAlbum(artist,album):
	results = getAlbum(album)
	return render_template('music.html',title=results['albumName'],songs=results['titles'],albumCovers=results['albums'],searchBoxText=results['albumName'])

@app.route('/music/search/all', methods=['POST'])
def musicSearchAll():
	results = musicSearchResults(True,'')
	return jsonify(**results)

@app.route('/music/playPause', methods=['POST'])
def playPauseMusic():
	queue.playPause()
	return ''

@app.route('/music/play', methods=['POST'])
def musicQueueThenPlay():
	artist = request.form['artist']
	title = request.form['title']
	album = request.form['album']
	playSong(queue.queueSong(artist,title,album))		#this will queue and play
	return '{"status": "done"}'

@app.route('/music/queue', methods=['POST'])
def musicQueue():
	artist = request.form['artist']
	title = request.form['title']
	album = request.form['album']
	queue.queueSong(artist,title,album)
	return '{"status": "done"}'

@app.route('/settings')
def settings():
	return render_template('settings.html',title='settings')

@app.route('/settings/libraryUpdate', methods=['POST'])
def libraryUpdate():
	(added, skipped, deleted, error) = scanMusicLibrary()
	if error == '':
		error = 'Done!'
	return error + ' - Added ' + str(added) + ' songs, skipped ' + str(skipped) + ' songs and deleted ' + str(deleted) + ' songs'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
