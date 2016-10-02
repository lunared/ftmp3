#! /bin/python3.5

from flask import Flask, render_template, request, send_from_directory, abort
import decimal
import glob
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.easyid3 import EasyID3 as ID3
import os, re
import base64

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

# add cover image reading
def read_cover_image(id3, key):
    apic = id3.getall(key)
    images = list(filter(lambda pic: pic.type == 3, apic))
    if len(images):
        return images[0]
    return None

ID3.RegisterKey('APIC', getter=read_cover_image)

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
            if song.tags.get('APIC'):
                cover = song.tags.get('APIC')
                info['cover'] = "data:{:s};base64,{:s}".format(cover.mime, base64.encodebytes(cover.data).decode('utf-8'))
        else:
            info = {
                'title': f,
                'album': '',
                'artist': ''
            }
        songs.append(info)

    return {
        'songs': sorted(songs, key=lambda song: (song['album'], song.get('track', '0'), song['artist'], song['title'])),
        'path': path
    }

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
