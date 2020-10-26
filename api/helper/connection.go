package helper

import (
	"fmt"
	"log"
	"os"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func ConnectDB() (db *mongo.Database, err error) {
	db_host, ok := os.LookupEnv("DB_HOST")
	if !ok {
		log.Fatalf("DB_HOST not set")
	} else {
		log.Printf("using %s for 'DB_HOST'", db_host)
	}
	client, err := mongo.NewClient(options.Client().ApplyURI(fmt.Sprintf("mongodb://%s", db_host)))

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB!")

	return client.Database("parts"), err
}
