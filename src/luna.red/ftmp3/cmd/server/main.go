package main

import (
	"flag"
	"html/template"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
	"luna.red/ftmp3/internal/server"
)

func main() {
	port := flag.String("-p", "8080", "port to run the server on")
	directory := flag.String("d", "~/Music", "music directory being served, including subdirectories")
	flag.Parse()

	fileserver := http.FileServer(http.Dir(*directory))
	staticfiles := http.FileServer(http.Dir("../../web/static"))

	t, err := template.ParseGlob("../../web/templates/*.html")
	if err != nil {
		panic(err)
	}

	router := mux.NewRouter()
	router.HandleFunc("/", routes.Index(*directory, t)).Methods("GET")
	router.PathPrefix("/__static__/").Handler(http.StripPrefix("/__static__", staticfiles))
	// stream files to clients
	router.HandleFunc("/{path:.*}/stream", routes.Stream(*directory, fileserver)).Methods("GET")
	router.HandleFunc("/{path:.*}/cover", routes.Cover(*directory, fileserver)).Methods("GET")
	// serve the ftmp3 website
	router.HandleFunc("/{path:.*}", routes.Index(*directory, t)).Methods("GET").Queries(
		"recurse", "{(true|false)?}",
	)

	http.Handle("/", router)
	http.ListenAndServe(strings.Join([]string{":", *port}, ""), nil)
}
