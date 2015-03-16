import pygame
from collections import OrderedDict

class Queue(object):

	def __init__(self):
		self.list = OrderedDict()
		self.musicPlaying = False
		self.current = ''
		self.repeat = True
		self.shuffle = True
		self.songRemoved = False

	def add(self, artist, title, album):
		self.list[artist+title] = {'artist': artist, 'title': title, 'album': album}
		print 'Added ' + title + ' by ' + artist

	def remove(self, artist, title):
		self.list.pop(artist+title)

	def nextPrev(self,direction): #returns next song, not shuffle and always repeat
		song = {}

		currentIndex = self.list.keys().index(self.current)
		totalLength = len(self.list)
		if direction == 'next':
			currentIndex = currentIndex + 1
		else:
			currentIndex = currentIndex - 1
		nextIndex = (currentIndex) % totalLength
		newSong = self.list[self.list.keys()[nextIndex]]

		song['artist'] = newSong['artist']
		song['title'] = newSong['title']
		
		print '>> Going to next song'

		return song

	def queueSong(self, artist,title,album):		#so this add song to queue if not in queue and returns song data
													#if in queue, does nothing... if not, adds it

		song = {}
		key = artist+title

		if key not in self.list:			##check here if song is in list, current index or add to end of list
			self.add(artist, title, album)

		song['artist'] = artist
		song['title'] = title

		return song

	def queueRemove(self, artist, title):
		key = artist + title
		del self.list[key]
		if self.current == key:
			self.songRemoved = True
			pygame.mixer.music.stop()

		print 'Removed ' + title + ' by ' + artist

		return

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

	def getList(self):
		results = {}
		results['titles'] = self.list.items()
		return self.list.items()