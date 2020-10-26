package helper

import (
	"os"
	"testing"
)

func TestConnectDB(t *testing.T) {
	os.Setenv("DB_HOST", "localhost:27017")
	db, err := ConnectDB()

	if err != nil {
		t.Fatalf("returned error %s", err)
	}
	want := "parts"
	got := db.Name()
	if want != got {
		t.Errorf("got %s wanted %s for db name", got, want)
	}
}
