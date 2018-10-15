package routes

import (
	"net/http"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/gorilla/mux"
	"luna.red/ftmp3/internal/mediameta"
)

func Stream(rootDir string, fileserver http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		path := filepath.Join(rootDir, filepath.Join(strings.Split(vars["path"], "/")...))

		isAudio, _ := regexp.MatchString(mediameta.ValidAudioFiles, path)
		// only serve audio files
		if isAudio {
			r.URL.Path = vars["path"]
			fileserver.ServeHTTP(w, r)
		} else {
			http.Error(w, "", 404)
		}
	}
}
