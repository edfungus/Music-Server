from app import db, app, queue
from .models import Library
from sqlalchemy import or_
from threading import Thread
import eyed3
import os
import pygame
import urllib2

import time

tester = 5

def test():
	global queue
	global tester
	tester = 6
	queue.current = 'sdfds'
	pygame.mixer.music.pause()


def playSong(song):			#receives data from queue.queue
	artist = song['artist']
	title = song['title']

	db_search = Library.query.filter_by(title=title, artist=artist).with_entities(Library.filename).first()
	try:
		pygame.mixer.music.load(os.path.join(app.config['MUSICDIR'],db_search.filename))
		pygame.mixer.music.play()
		queue.musicPlaying = True
		queue.current = artist+title
		print 'Playing ' + title + ' by ' + artist
	except:
		print 'Could not play file: ' + title + ' by ' + artist + '. DB search is ' + str(db_search)

	
	time.sleep(5)
	testthread = Thread(target=test)
	testthread.start()
	print queue.current
	print tester

	return

def getArtist(artist):
	results = {}
	results['titles'] = Library.query.filter_by(artistURL=artist).order_by(Library.title).all()
	results['albums'] = Library.query.filter_by(artistURL=artist).with_entities(Library.artist, Library.album, Library.artwork, Library.artwork, Library.artistURL, Library.albumURL).order_by(Library.album).distinct().all()
	results['artistName'] = results['titles'][0].artist
	return results

def getAlbum(album):
	results = {}
	results['titles'] = Library.query.filter_by(albumURL=album).order_by(Library.title).all()
	results['albums'] = Library.query.filter_by(albumURL=album).with_entities(Library.artist, Library.album, Library.artwork, Library.artistURL, Library.albumURL).order_by(Library.album).distinct().all()
	results['albumName'] = results['titles'][0].album
	return results

def musicSearchResults(all,query):	#this is getting a list of songs (with artist and album..) basically the song listing of the search function
	if all:			#just get me all the songs for basic listing
		results = {}
		results['titles'] = Library.query.with_entities(Library.id, Library.title, Library.artist, Library.album, Library.artistURL, Library.albumURL).order_by(Library.title).all()
		return results
	else:
		queryWord = query.split(' ')
		results = {}

		db_lookup = db.session.query(Library)
		for value in queryWord:
			db_lookup = db_lookup.filter(or_(getattr(Library, 'title').like("%%%s%%" % value), getattr(Library, 'artist').like("%%%s%%" % value)))
    	results['titles'] = db_lookup.with_entities(Library.id, Library.title, Library.artist, Library.album, Library.artistURL, Library.albumURL).order_by(Library.title).distinct().all()

    	db_lookup = db.session.query(Library)
    	for value in queryWord:
			db_lookup = db_lookup.filter(getattr(Library, 'artist').like("%%%s%%" % value))
    	results['artists'] = db_lookup.with_entities(Library.artist, Library.artistURL).order_by(Library.artist).distinct().all()

    	db_lookup = db.session.query(Library)
    	for value in queryWord:
			db_lookup = db_lookup.filter(or_(getattr(Library, 'album').like("%%%s%%" % value), getattr(Library, 'artist').like("%%%s%%" % value)))
    	results['albums'] = db_lookup.with_entities(Library.artist, Library.album, Library.artwork, Library.artistURL, Library.albumURL).order_by(Library.album).distinct().all()

    	return results

def scanMusicLibrary():		#skips and delete files (keeps the files and database in sync)		
	added = 0
	skipped = 0
	deleted = 0
	error = ''

	fullMusicPath = app.config['MUSICDIR'] + '/'
	fullArtworkPath = app.config['ARTWORKDIR'] + '/'

	db_dump = Library.query.all()

	for file in os.listdir(app.config['MUSICDIR']):
		if file.endswith(".mp3"):
			song = eyed3.load(fullMusicPath + file)
			tag = song.tag

			title = tag.title
			artist = tag.artist
			artistURL = artist.replace(" ", "")

			check = False			#Is the song in the dump? .. no until proven otherwise
			
			for song in db_dump:			
				if song.title == title and song.artist == artist:
					db_dump.remove(song)	#remove from list if removed from folder
					check = True
			
			if check is False:		#yup, this file has not been added before	
				album = tag.album
				albumURL = album.replace(" ", "")
				track = tag.track_num[0]
				artwork = ''
				for imageInfo in tag.images:
					if imageInfo.picture_type == 3:		#this checks for the front cover
						if imageInfo.mime_type == 'image/jpeg':
							ext = '.jpg'
						elif imageInfo.mime_type == 'image/png':
							ext = '.png'
						else: 
							error = 'Unkown album art format'
							print 'Unknown album art image type: ' + imageInfo.mime_type
						artwork = artist + album + ext
						artwork = artwork.replace(" ", "")
						artworkData = imageInfo.image_data
						if not os.path.isfile(fullArtworkPath + artwork):	#if cover is not extracted, do it now
							with open(fullArtworkPath + artwork, 'w') as f:
			    					f.write(artworkData)				
							print 'Added artwork: ' + artwork
				if artwork == '':
					artwork = 'default_album_art.png'

				newSong = Library(filename=file,title=title,artist=artist,artistURL=artistURL,album=album,albumURL=albumURL,artwork=artwork,track=track,fav=False)
				db.session.add(newSong)	
				db.session.commit()		
				added = added + 1
				print 'Added song to DB: ' + title + ' by ' + artist
			
			else:
				skipped = skipped + 1

	if db_dump:
		removeAlbumArt = []
		for song in db_dump:
			removeAlbumArt.append(song.artwork)			#append artwork so that we can delete it if necessary
			db.session.query(Library).filter_by(title=song.title, artist=song.artist).delete()
			db.session.commit()
			deleted = deleted + 1
			print 'Removed song from DB: ' + song.title + ' by ' + song.artist

		keys = {}			#delete leftover album artworks
		for e in removeAlbumArt:
			keys[e] = 1
		removeAlbumArtUnqiue = keys.keys()

		for filename in removeAlbumArtUnqiue:
			artCheck = Library.query.filter_by(artwork=filename).first()	#make sure no other songs from that album is on here
			if artCheck is None:
				os.remove(fullArtworkPath + filename)
				print 'Removed artwork: ' + filename

	return (added, skipped, deleted, error)
