from flask import Flask, render_template, request, send_from_directory, abort, send_file
from mutagen.mp3 import EasyMP3 as MP3
import os
import re

from .app import app
from .files import get_songs


COVER_FORMAT = re.compile(r"^(?i)cover\.jpg$")

@app.route('/<path:path>/cover')
def cover(path):
    """
    Gets the cover image for a shared song
    """
    songpath = "{0}{1}".format(app.config['MUSIC_DIRECTORY'], path)
    song = MP3(songpath)
    cover = None
    mime = 'image/jpeg'
    
    try:
        if song.tags:
            if song.tags.get('cover'):
                cover_meta = song.tags.get('cover')
                cover = io.BytesIO(cover_meta.data)
                mime = cover_meta.mime
    except:
        # in case data didn't parse correctly we can still try and get a cover.jpg if one exists
        pass

    # check for cover.jpg if not in meta tags
    if not cover:
        # allow for case insensitive searching for cover.jpg
        for f in os.listdir(os.path.dirname(songpath)):
            if COVER_FORMAT.match(f):
                return send_file(os.path.join(os.path.dirname(songpath), f), mimetype=mime)

    return abort(404)


@app.route('/')
@app.route('/<path:path>')
def home(path=None):
    if path and not os.path.exists(os.path.join(app.config['MUSIC_DIRECTORY'], path)):
        return abort(404)
    if app.config['SERVE_FILES'] and path and app.config['FORMAT_MATCH'].search(path):
        return send_from_directory(app.config['MUSIC_DIRECTORY'], path)
    context = get_songs(path)
    return render_template("body.html", **context), 200
