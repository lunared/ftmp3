# ftmp3

This project provides an html5 audio player and super basic interface for playing mp3 (and some other audio files) off of an FTP.

Designed to play along with html5 ftp clients, such as [Cute File Browser](https://github.com/martinaglv/cute-files).

## How to use
As a golang app, just build it or run it directly from the command line.

```
go build luna.red/ftmp3
```

### Settings


| Key | Type | Default | Description |
| --- | --- | --- | --- | 
| -d | filepath | ~/Music | The root filepath of the music files to be served |
| --p  | int      | 8080 | Port number to host the app on |


These args can be used to configure the applicaiton.

I recommended setting up Cute File Browser and ftmp3 with nginx in a smart way so you can hop between them quickly.  
eg. `http://0.0.0.0/share/my-music-folder` to `http://0.0.0.0/mp3/my-music-folder`
