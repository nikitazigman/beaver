package main

import (
	"beaver-api/internal/storage"
	"context"
	"fmt"
	"os"

	"github.com/jackc/pgx/v5"
)

const (
	fmtDBString = "host=%s user=%s password=%s dbname=%s port=%d sslmode=disable"
	host = "localhost"
	user = "beaver_api"
	password = "beaver_api"
	dbname = "beaver_api_db"
	port = 5432
)


func main() {
	url := fmt.Sprintf(fmtDBString, host,user,password,dbname,port)

	conn, err := pgx.Connect(context.Background(), url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())

	s := storage.New(conn)
	fmt.Println(s)
}
