#! /bin/python3.5

from flask import Flask, render_template, request, send_from_directory, abort, send_file
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.easyid3 import EasyID3 as ID3
import decimal
import glob
import os
import re
import io
import base64
import fnmatch

app = Flask(__name__,)

# Root directory that we scan for music from
# Do not change this unless you're not using the docker-compose
# It is preferred you use just change the volume mapping on the docker-compose.yml
MUSIC_DIRECTORY = "/media/Music/"
# Tells flask to serve the mp3 files
# Typically you'd want nginx to do this instead, as this is an
# easy way to cause concurrent response issues with flask
SERVE_FILES = False
# acceptable standard html5 compatible formats
FORMAT_MATCH = re.compile(r"\.(mp3|ogg|midi|mid)$")


# when starting up the app, we make sure we cache the directory tree of all folders
# that may be traversed by ftmp3.  This allows us to have a nice navigation menu
# of the file system.
def get_dir_tree():
    tree = []
    for path, dirs, files in os.walk(MUSIC_DIRECTORY):
        if len(fnmatch.filter(files, '*.mp3')) > 0:
            if not path.endswith('/'):
                path += '/'
            tree.append(path[len(MUSIC_DIRECTORY):])
    return tree
DIR_TREE = get_dir_tree()

# add cover image reading
def read_cover_image(id3, key):
    apic = id3.getall('APIC')
    images = list(filter(lambda pic: pic.type == 3, apic))
    if len(images):
        return images[0]
    return None

ID3.RegisterKey('cover', getter=read_cover_image)

def get_songs(path):
    filepath = "{0}".format(MUSIC_DIRECTORY)
    if path:
        filepath = "{0}{1}".format(MUSIC_DIRECTORY, path)
    files = [f for f in os.listdir(filepath) if FORMAT_MATCH.search(f)]
    songs = []
    for f in files:
        songpath = "{0}{1}".format(filepath, f)
        song = MP3(songpath)
        if song.tags:
            info = {
                'artist':song.tags.get('artist', [''])[0],
                'title':song.tags.get('title', [f])[0],
                'track':song.tags.get('tracknumber', [''])[0],
                'album':song.tags.get('album', [''])[0],
                'length':"{0}:{1:02d}".format(int(song.info.length//60), int(song.info.length%60)),
                'path':f,
            }
            if song.tags.get('cover'):
                cover = song.tags.get('cover')
                info['cover'] = "{:s}/cover".format(f)
        else:
            info = {
                'title': f,
                'album': '',
                'artist': ''
            }
        songs.append(info)

    return {
        'songs': sorted(songs, key=lambda song: (song['album'], song.get('track', '0'), song['artist'], song['title'])),
        'path': path,
        'tree': DIR_TREE
    }

@app.route('/<path:path>/cover')
def cover(path):
    """
    Gets the cover image for a shared song
    """
    songpath = "{0}{1}".format(MUSIC_DIRECTORY, path)
    song = MP3(songpath)
    if song.tags:
        if song.tags.get('cover'):
            cover = song.tags.get('cover')
            return send_file(io.BytesIO(cover.data),
                             mimetype=cover.mime)
    return None, status.HTTP_404_NOT_FOUND


@app.route('/')
@app.route('/<path:path>')
def home(path=None):
    if path and not os.path.exists(os.path.join(MUSIC_DIRECTORY, path)):
        return abort(404)
    if SERVE_FILES and path and FORMAT_MATCH.search(path):
        return send_from_directory(MUSIC_DIRECTORY, path)
    context = get_songs(path)
    return render_template("body.html", **context), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
