package helper

import (
	"fmt"
	"log"
	"os"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func ConnectDB() (db *mongo.Database, err error) {
	dbHost, ok := os.LookupEnv("DB_HOST")
	if !ok {
		log.Fatalf("DB_HOST not set")
	} else {
		log.Printf("using %s for 'DB_HOST'", dbHost)
	}
	client, err := mongo.NewClient(options.Client().ApplyURI(fmt.Sprintf("mongodb://%s", dbHost)))

	if err != nil {
		log.Fatal(err)
	}

	log.Println("Connected to MongoDB!")

	return client.Database("parts"), err
}
