from mutagen.mp3 import EasyMP3 as MP3
from mutagen.easyid3 import EasyID3 as ID3
from mutagen.id3 import PictureType
from mutagen.mp3 import HeaderNotFoundError
from .app import app
import decimal
import glob
import os
import re
import io
import base64
import fnmatch
from urllib.request import pathname2url
from pathlib import Path

config = app.config

def read_cover_image(id3, key):
    """
    add cover image reading from mp3s
    """
    apic = id3.getall('APIC')
    images = sorted(
        list(filter(lambda pic: pic.type in [PictureType.OTHER, PictureType.COVER_FRONT], apic)),
        key=(lambda pic: -pic.type)
    )
    if len(images):
        return images[0]
    return None
ID3.RegisterKey('cover', getter=read_cover_image)


# allow for case insensitive searching for cover.jpg
COVER_FORMAT = re.compile(r"^(?i)cover\.jpg$")

def get_cover(songpath):
    """
    Get the safest file/data to use as the cover image
    """
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
        pass

    # check for cover.jpg if not in meta tags
    if not cover:
        def search(path, i):
            """
            Recursively search parent directories for a cover.jpg
            """
            if i > config['COVER_IMG_RECURSION_LIMIT']:
                return None

            for file in os.listdir(path):
                if COVER_FORMAT.match(file):
                    return os.path.join(path, file)
            return search(os.path.dirname(path), i + 1)

        cover = search(os.path.dirname(songpath), 0)
    return cover, mime

def get_info(filepath, songfile):
    """
    Get the song's metadata for display on the page
    """
    songpath = Path(filepath, songfile)
    url = "/"+pathname2url(songpath.relative_to(config['MUSIC_DIRECTORY']).as_posix())
    try:
        song = MP3(songpath.as_posix())
    except HeaderNotFoundError:
        print("mutagen.mp3.HeaderNotFoundError for {}".format(songpath))
        song = None
    if getattr(song, "tags", None):
        info = {
            'artist':song.tags.get('artist', [''])[0],
            'title':song.tags.get('title', [songfile])[0],
            'track':song.tags.get('tracknumber', [''])[0],
            'album':song.tags.get('album', [''])[0],
            'length':"{0}:{1:02d}".format(int(song.info.length//60), int(song.info.length%60)),
            'path': url,
        }
    else:
        info = {
            'title': songfile,
            'album': '',
            'artist': '',
            'path': url,
        }
    return info

