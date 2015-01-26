Music Server
Edmund Fung - 2014

This is running off Flask in virtualenv. Use 'source env/bin/activate' to activate this virtualenv for this instance of terminal

packages:
pip install flask-sqlalchemy
pip install eyed3
pip install sqlalchemy-migrate
get pygame (http://stackoverflow.com/questions/17869101/unable-to-install-pygame-using-pip)


to do... basically push the music queueing to another thread so that a function will know when the music is finished and will call queue.next() to get the next song and play it
