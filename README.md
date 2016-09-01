# ftmp3

This project provides an html5 audio player and super basic interface for playing mp3 (and some other audio files) off of an FTP.

Designed to play along with html5 ftp clients, such as [Cute File Browser](https://github.com/martinaglv/cute-files).

## How to use

Build and run the container (docker-compose build && docker-compose up -d).  Be sure to configure the volume on the docker-compose file to be equal to the files that are exposed by your FTP.
By default the docker-container will render the site on port 80.  You'll probably want to change that, unless you're running this on a subdomain.

Alternatively, since this is a really simple app, you can just `pip install -r requirements.txt` and then `python app.py` and you'll be set.  You'll have to edit the app.py in this case to change the ftp directory.  It's also mapped to the default port 5000.

I recommended setting up Cute File Browser and ftmp3 with nginx in a smart way so you can hop between them quickly.  
eg. `0.0.0.0/share/my-music-folder` to `0.0.0.0/mp3/my-music-folder`

## Links

http://flask.pocoo.org/
https://github.com/devsnd/tinytag/
