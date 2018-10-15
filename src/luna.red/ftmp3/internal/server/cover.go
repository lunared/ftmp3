package routes

import (
	"net/http"
	"path/filepath"
	"strings"

	"github.com/gorilla/mux"
	"luna.red/ftmp3/internal/mediameta"
)

func Cover(rootDir string, fileserver http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		path := filepath.Join(rootDir, filepath.Join(strings.Split(vars["path"], "/")...))

		if cover := mediameta.GetCover(path); cover != nil {
			w.Write(cover)
		} else {
			// check to see if there's a cover.jpg file in the folder

			http.NotFound(w, r)
		}
	}
}
