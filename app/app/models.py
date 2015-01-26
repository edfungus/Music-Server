from app import db

class Library(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(128), index=True, unique=False)
	title = db.Column(db.String(128), index=True, unique=False)
	artist = db.Column(db.String(128), index=True, unique=False)
	artistURL = db.Column(db.String(128), index=True, unique=False)
	album = db.Column(db.String(128), index=True, unique=False)
	albumURL = db.Column(db.String(128), index=True, unique=False)
	artwork = db.Column(db.String(128), index=True, unique=False)
	track = db.Column(db.Integer, index=True, unique=False)
	fav = db.Column(db.Boolean, index=True, unique=False)

	
		
	def __repr__(self):
		return '<title %r - artist %r - album %r - fav %r>' % (self.title,self.artist,self.album,self.fav)


