package api

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/", HomeHandler)
	r.HandleFunc("/list", GetParts).Methods("GET")
	r.HandleFunc("/list/{id}", GetPart).Methods("GET")
	r.HandleFunc("/add", AddPart).Methods("POST")
	r.HandleFunc("/update/{id}", UpdatePart).Methods("POST")

	log.Fatal(http.ListenAndServe(":8000", r))
}
