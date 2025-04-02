package main

import (
	"beaver-api/internal/api/storage"
	"fmt"
	"log"
)

func main() {
	db, err := storage.NewDB("localhost", 5432, "postgres", "postgres", "beaver")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(db)
}
