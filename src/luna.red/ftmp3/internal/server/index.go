package routes

import (
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/gorilla/mux"
	"luna.red/ftmp3/internal/mediameta"
)

type Subdirectory struct {
	Name        string
	Path        string
	Songs       int
	Directories int
	Playlists   int
}

type MediaContext struct {
	Subdirectories []Subdirectory
	Songs          []mediameta.SongMetadata
	Playlists      []string
	Path           string
	Parent         string
	Recurse        bool
	ProgressSteps  []float32
}

func recurseFiles(rootDir string, target string, context *MediaContext) {
	filepath.Walk(target, func(path string, info os.FileInfo, err error) error {
		// ignore dirs
		if info.IsDir() {
			return nil
		}

		isAudio, _ := regexp.MatchString(mediameta.ValidAudioFiles, info.Name())
		if isAudio {
			// attempt to parse metadata
			meta := mediameta.ParseMetadata(path)
			rel, _ := filepath.Rel(rootDir, path)
			meta.Filename = filepath.ToSlash(rel)
			context.Songs = append(context.Songs, meta)
		}
		return nil
	})
}

func normalFiles(rootDir string, target string, context *MediaContext) {
	// get all files in folder
	files, _ := ioutil.ReadDir(target)
	for _, info := range files {
		toFile := filepath.Join(target, info.Name())
		isAudio, _ := regexp.MatchString(mediameta.ValidAudioFiles, info.Name())
		if isAudio {
			// attempt to parse metadata
			meta := mediameta.ParseMetadata(toFile)
			rel, _ := filepath.Rel(rootDir, toFile)
			meta.Filename = filepath.ToSlash(rel)
			context.Songs = append(context.Songs, meta)
		}
		if info.IsDir() {
			rel, _ := filepath.Rel(rootDir, toFile)
			subdir := Subdirectory{
				info.Name(),
				filepath.ToSlash(rel),
				0,
				0,
				0,
			}
			files, _ := ioutil.ReadDir(target)
			for _, info := range files {
				if info.IsDir() {
					subdir.Directories++
				}
				isAudio, _ := regexp.MatchString(mediameta.ValidAudioFiles, target)
				if isAudio {
					subdir.Songs++
				}
			}
			context.Subdirectories = append(context.Subdirectories, subdir)
		}
	}
}

func Index(rootDir string, t *template.Template) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		target := filepath.Join(rootDir, filepath.Join(strings.Split(vars["path"], "/")...))
		recurse := r.URL.Query().Get("recurse")
		steps := make([]float32, 50)
		for i := 0; i < 50; i++ {
			steps[i] = float32(i) / float32(50.0)
		}

		context := MediaContext{
			make([]Subdirectory, 0),
			make([]mediameta.SongMetadata, 0),
			make([]string, 0),
			vars["path"],
			path.Dir(vars["path"]),
			recurse == "true",
			steps,
		}

		if info, err := os.Stat(target); err != nil {
			log.Panic(err)
		} else if info != nil && info.IsDir() {
			if recurse == "true" {
				recurseFiles(rootDir, target, &context)
			} else {
				normalFiles(rootDir, target, &context)
			}
			if err := t.ExecuteTemplate(w, "body.html", context); err != nil {
				log.Fatal(err)
			}
		} else {
			http.NotFound(w, r)
		}
	}
}
