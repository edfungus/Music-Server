import os

basedir = os.path.abspath(os.path.dirname(__file__))
MUSICDIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'music_files'))
ARTWORKDIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'app/static/music_artwork'))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

