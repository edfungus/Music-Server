Music Server
Edmund Fung - 2014

This is running off Flask in virtualenv. Use 'source env/bin/activate' to activate this virtualenv for this instance of terminal

packages:
pip install flask-sqlalchemy
pip install eyed3
pip install sqlalchemy-migrate
get pygame (http://stackoverflow.com/questions/17869101/unable-to-install-pygame-using-pip)

Bugs:
	-Some Muse songs add twice??

To Do:
	-Make current song highlighted with socketIO
	-Update this git.. haha
	-Creating sorting on music page

Done:
	-Scans music in folder and adds them. Can also delete db entry when file is gone.
	-Grabs ID3 tags
	-Plays queued music in loop with no shuffle
	-Cool live search
	-Play/pause, next control
