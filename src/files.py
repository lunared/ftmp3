
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
"""
sorting precedence of the playlist
"""
match_file = lambda f : config['FORMAT_MATCH'].search(f)
"""
Determine if a file matches what is acceptable for ftmp3 to display
"""

def get_songs(path, recurse=False):
    """
    Gets the song listing for a directory
    Includes subdirectories as well.abort

    :param path - the file path to list from
    :param recurse - boolean indicating if we should recurse the tree for files
    """
    filepath = "{0}".format(config['MUSIC_DIRECTORY'])
    if path:
        filepath = os.path.join(config['MUSIC_DIRECTORY'], path)

    songs = []
    if recurse:
        for root, subdirs, files in os.walk(filepath):
            for f in filter(match_file, files):
                songs.append(get_info(root, f))
    else:
        files = filter(match_file, os.listdir(filepath))
        for f in files:
            songs.append(get_info(filepath, f))

    return {
        'songs': sorted(songs, key=order_by),
        'subdirectories': [{
            'path': os.path.join(filepath, dir)[len(config['MUSIC_DIRECTORY']):],
            'name': os.path.basename(dir),
            'songs': len(list(filter(
                match_file,
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
        ))] if not recurse else None,
        'recurse': recurse,
        'playlists': list(filter(lambda f: f.endswith("m3u"), os.listdir(filepath))),
        'path': path,
        'parent': os.path.join(filepath, os.pardir)[len(config['MUSIC_DIRECTORY']):]+"/"
    }
