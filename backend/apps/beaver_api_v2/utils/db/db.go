package db

import (
	"context"
	"fmt"
	"log"

	"github.com/jackc/pgx/v5/pgxpool"
)

const (
	fmtDBString = "host=%s user=%s password=%s dbname=%s port=%d sslmode=disable"
)

func New(host, user, password, dbname string, port int) *pgxpool.Pool {
	url := fmt.Sprintf(fmtDBString, host, user, password, dbname, port)

	pool, err := pgxpool.New(context.Background(), url)
	if err != nil {
		log.Fatal("Cannot establish connection with the database", host, dbname, user, port)
	}

	return pool
}
