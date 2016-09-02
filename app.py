#! /bin/python3.5

from flask import Flask, render_template, request, send_from_directory, abort
import decimal
import glob
import tinytag
import os, re

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


def get_songs(path):
    filepath = "{0}".format(MUSIC_DIRECTORY)
    if path:
        filepath = "{0}{1}".format(MUSIC_DIRECTORY, path)
    files = [f for f in os.listdir(filepath) if FORMAT_MATCH.search(f)]
    #raise ValueError(files)
    songs = []
    for file in files:
        songpath = "{0}{1}".format(filepath, file)
        #raise ValueError(songpath)
        song = tinytag.TinyTag.get(songpath)
        songs.append({
            'artist':song.artist if song.artist else "",
            'title':song.title,
            'track':song.track if song.track else "",
            'album':song.album if song.album else "",
            'length':"{0}:{1:02d}".format(int(song.duration//60), int(song.duration%60)),
            'path':file
        })

    return {
        'songs': sorted(songs, key=lambda song: (song['album'], int(song['track'] if song['track'] else 0), song['artist'], song['title'])),
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
