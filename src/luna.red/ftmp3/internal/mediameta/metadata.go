package mediameta

import (
	"fmt"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/bogem/id3v2"
)

type SongMetadata struct {
	Filename string
	Title    string
	Length   string
	Artist   string
	Album    string
	Track    string
}

func (s SongMetadata) Duration() string {
	if s.Length != "" {
		ms, _ := strconv.Atoi(s.Length)
		sec := int32((ms / 1000.0) % 60.0)
		min := int32(ms / 60000.0)
		return fmt.Sprintf("%02d:%02d", min, sec)
	}
	return ""
}

var ValidAudioFiles = "(mp3|ogg|flac|wav)$"

var parseOptions = id3v2.Options{
	Parse: true,
}

func GetCover(path string) []byte {
	tag, err := id3v2.Open(path, parseOptions)
	if err != nil {
		return nil
	}
	defer tag.Close()

	pictures := tag.GetFrames(tag.CommonID("Attached picture"))
	for _, f := range pictures {
		pic, ok := f.(id3v2.PictureFrame)
		if ok {
			return pic.Picture
		}
	}
	return nil
}

func ParseMetadata(path string) SongMetadata {
	filename := filepath.Base(path)
	tag, err := id3v2.Open(path, parseOptions)
	if err != nil {
		//log.Print(err)
		return SongMetadata{
			path,
			filename[0 : len(filename)-len(filepath.Ext(filename))],
			"",
			"",
			"",
			"",
		}
	}
	defer tag.Close()

	//every now and then we can parse the id3 tag but it'll return blank values
	title := strings.TrimSpace(tag.Title())
	if title == "" {
		title = filename[0 : len(filename)-len(filepath.Ext(filename))]
	}

	return SongMetadata{
		path,
		title,
		strings.TrimSpace(tag.GetTextFrame(tag.CommonID("Length")).Text),
		strings.TrimSpace(tag.Artist()),
		strings.TrimSpace(tag.Album()),
		strings.TrimSpace(tag.GetTextFrame("TRCK").Text),
	}
}
