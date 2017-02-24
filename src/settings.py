import re
import os

# Root directory that we scan for music from
# Do not change this unless you're not using the docker-compose
# It is preferred you use just change the volume mapping on the docker-compose.yml
MUSIC_DIRECTORY = os.environ.get("FTMP3_MUSIC", "/media/Music")
# Tells flask to serve the mp3 files
# Typically you'd want nginx to do this instead, as this is an
# easy way to cause concurrent response issues with flask
SERVE_FILES = True
# acceptable standard html5 compatible formats
FORMAT_MATCH = re.compile(r"\.(mp3|ogg|midi|mid)$")
