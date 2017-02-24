from flask import Flask, render_template, request, send_from_directory, abort, send_file
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.easyid3 import EasyID3 as ID3
from mutagen.id3 import PictureType
import decimal
import glob
import os
import re
import io
import base64
import fnmatch

# add cover image reading
def read_cover_image(id3, key):
    apic = id3.getall('APIC')
    images = sorted(
        list(filter(lambda pic: pic.type in [PictureType.OTHER, PictureType.COVER_FRONT], apic)),
        key=(lambda pic: -pic.type)
    )
    if len(images):
        return images[0]
    return None

ID3.RegisterKey('cover', getter=read_cover_image)