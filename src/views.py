from flask import Flask, render_template, request, send_from_directory, abort, send_file
import os
import re

from .app import app
from .files import get_songs
from .song import get_cover

@app.route('/<path:path>/cover')
def cover(path):
    """
    Gets the cover image for a shared song
    """
    songpath = os.path.join(app.config['MUSIC_DIRECTORY'], path)
    cover, mime = get_cover(songpath)
    if cover:
        return send_file(cover, mimetype=mime)

@app.route('/<path:path>/stream')
def stream(path):
    if app.config['SERVE_FILES'] and path and app.config['FORMAT_MATCH'].search(path):
        return send_from_directory(app.config['MUSIC_DIRECTORY'], path)
    return abort(401)

@app.route('/')
@app.route('/<path:path>')
def home(path=None):
    if path and not os.path.exists(os.path.join(app.config['MUSIC_DIRECTORY'], path)):
        return abort(404)
    context = get_songs(path, recurse=request.args.get('recurse', False))
    return render_template("body.html", **context), 200


@app.route('/__static__/<path:path>')
def staticfiles(path):
    return send_from_directory('../static', path)
