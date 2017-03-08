
from flask import Flask, render_template, request, send_from_directory, abort, send_file, config
import decimal
import glob
import os
import re
import io
import base64
import fnmatch

from .app import app
from .song import get_info

config = app.config
order_by = lambda song: (song['album'], song.get('track', '0'), song['artist'], song['title'])

def get_dir_tree():
    """
    When starting up the app, we make sure we cache the directory tree of all folders
    that may be traversed by ftmp3.
    """

    tree = []
    for path, dirs, files in os.walk(config['MUSIC_DIRECTORY']):
        if len(fnmatch.filter(files, '*.mp3')) > 0:
            if not path.endswith('/'):
                path += '/'
            tree.append(path[len(config['MUSIC_DIRECTORY']):])
    return tree
DIR_TREE = get_dir_tree()

def get_songs(path):
    filepath = "{0}".format(config['MUSIC_DIRECTORY'])
    if path:
        filepath = os.path.join(config['MUSIC_DIRECTORY'], path)
    files = filter(lambda f: config['FORMAT_MATCH'].search(f), os.listdir(filepath))
    songs = []
    for f in files:
        songs.append(get_info(filepath, f))

    return {
        'songs': sorted(songs, key=order_by),
        'subdirectories': [{
            'path': os.path.join(filepath, dir)[len(config['MUSIC_DIRECTORY']):],
            'name': os.path.basename(dir),
            'songs': len(list(filter(
                lambda x: config['FORMAT_MATCH'].search(x),
                os.listdir(os.path.join(filepath, dir))
            ))),
            'directories': len(
                list(filter(
                    lambda x: os.path.isdir(os.path.join(filepath, dir, x)),
                    os.listdir(os.path.join(filepath, dir))
                ))
            ),
            'playlists': len(
                list(filter(
                    lambda x: x.endswith("m3u"),
                    os.listdir(os.path.join(filepath, dir))
                ))
            )
        } for dir in list(filter(
            lambda f: os.path.isdir(os.path.join(filepath, f)),
            os.listdir(filepath)
        ))],
        'playlists': list(filter(lambda f: f.endswith("m3u"), os.listdir(filepath))),
        'path': path,
        'parent': os.path.join(filepath, os.pardir)[len(config['MUSIC_DIRECTORY']):]+"/"
    }
