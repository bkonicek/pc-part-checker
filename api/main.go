package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/bkonicek/pricecheck-api/models"
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
)

func getenv(key, fallback string) string {
	value := os.Getenv(key)
	if len(value) == 0 {
		return fallback
	}
	return value
}

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatalf("error loading .env file")
	}

	r := mux.NewRouter()
	// r.HandleFunc("/", HomeHandler)
	r.HandleFunc("/list", GetParts).Methods("GET")
	r.HandleFunc("/list/{id}", GetPart).Methods("GET")
	r.HandleFunc("/add", AddPart).Methods("POST")
	r.HandleFunc("/update/{id}", UpdatePart).Methods("POST")

	log.Fatal(http.ListenAndServe(":8000", r))
}

// GetParts handles GET requests to the /list path and returns
// all parts from the database
func GetParts(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "Parts List\n")
}

// GetPart handles GET requests to the /list/{id} path and
// returns a single part matching the ID in the request
func GetPart(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	fmt.Fprintf(w, "Found part ID %s\n", vars["id"])
}

// parseJSON takes json-formatted input and
// parses it into a Part struct
func parseJSON(j io.ReadCloser) *models.Part {
	decoder := json.NewDecoder(j)

	var p models.Part
	err := decoder.Decode(&p)

	if err != nil {
		panic(err)
	}
	return &p
}

// AddPart handles POST requests on the /add path and adds
//  a part to the database using the body of the request
func AddPart(w http.ResponseWriter, r *http.Request) {
	p := parseJSON(r.Body)
	fmt.Printf("Added %s: $%d", p.Name, p.Price)
}

// UpdatePart handles requests to the /update/{id} path
// and updates the given ID's name and price
func UpdatePart(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	p := parseJSON(r.Body)
	fmt.Printf("Updated id %s: name: %s new price is $%d", vars["id"], p.Name, p.Price)
}
