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

	port := fmt.Sprintf("%s", getenv("API_PORT", "8000"))
	fmt.Printf("Listening on %s\n", port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", port), r))
}

func GetParts(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "Parts List\n")
}

func GetPart(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	fmt.Fprintf(w, "Found part ID %s\n", vars["id"])
}

func parseJson(j io.ReadCloser) *models.Part {
	decoder := json.NewDecoder(j)

	var p models.Part
	err := decoder.Decode(&p)

	if err != nil {
		panic(err)
	}
	return &p
}

func AddPart(w http.ResponseWriter, r *http.Request) {
	p := parseJson(r.Body)
	fmt.Printf("Added %s: $%d", p.Name, p.Price)
}

func UpdatePart(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	p := parseJson(r.Body)
	fmt.Printf("Updated id %s: name: %s new price is $%d", vars["id"], p.Name, p.Price)
}
