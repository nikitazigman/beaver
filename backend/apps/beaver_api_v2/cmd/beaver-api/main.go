package main

import (
	"beaver-api/internal/app"
	"beaver-api/internal/business"
	"beaver-api/internal/storage"
	"context"
	"fmt"
	"log"
	"net/http"
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

	tr := storage.New(conn)
	ts := business.NewTagService(tr)
	r := app.New(ts)

	s := &http.Server{
		Addr:         fmt.Sprintf(":%d", 8000),
		Handler:      r,
	}

	log.Println("Starting server " + s.Addr)
	if err := s.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatal("Server startup failed")
	}
}
