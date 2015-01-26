import pygame

class Queue(object):

	def __init__(self):
		self.list = {}
		self.musicPlaying = False
		self.current = ''

	def add(self, artist, title, album):
		self.list[artist+title] = {'artist': artist, 'title': title, 'album': album}
		print 'added'

	def remove(self, artist, title):
		self.list.pop(artist+title)

	def next(self):
		return

	def queueSong(self, artist,title,album):		#so this add song to queue if not in queue and returns song data
													#if in queue, does nothing... if not, adds it

		song = {}
		key = artist+title

		if key not in self.list:			##check here if song is in list, current index or add to end of list
			self.add(artist, title, album)

		song['artist'] = artist
		song['title'] = title

		print self.list

		return song

	def removeAll(self):
		self.list = {}

	def playPause(self):
		if self.musicPlaying:
			pygame.mixer.music.pause()
			self.musicPlaying = False
		else:
			pygame.mixer.music.unpause()
			self.musicPlaying = True
		return

	def list(self):
		return self.list