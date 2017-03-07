# ftmp3

This project provides an html5 audio player and super basic interface for playing mp3 (and some other audio files) off of an FTP.

Designed to play along with html5 ftp clients, such as [Cute File Browser](https://github.com/martinaglv/cute-files).

## How to use
### Docker
Build and run the container
```
docker-compose build && docker-compose up -d
```

Be sure to configure the volume on the docker-compose file to be equal to the files that are exposed by your FTP.
You can configure the port and volume map within the .env file used by docker-compose.

### Flask
Alternatively, since this is a really simple app, you can just run it directly on your host machine.
```
pip install -r requirements.txt
``` 
```
python app.py
```

### Settings


| Key | Type | Default | Description |
| --- | --- | --- | --- | 
| FTMP3_MUSIC | filepath | /media/Main | The root filepath of the music files to be served |
| FTMP3_PORT  | int      | 8080 | Port number to host the app on |


These environment variables can be used when hosting without docker as well as within the .env file of docker-compose to
configure the applicaiton.

I recommended setting up Cute File Browser and ftmp3 with nginx in a smart way so you can hop between them quickly.  
eg. `http://0.0.0.0/share/my-music-folder` to `http://0.0.0.0/mp3/my-music-folder`
