package db

import (
	"context"
	"fmt"
	"log"

	"github.com/jackc/pgx/v5/pgxpool"
)

const (
	fmtDBString = "host=%s user=%s password=%s dbname=%s port=%d sslmode=%s"
)

func New(host, user, password, dbname, sslmode string, port int) *pgxpool.Pool {
	url := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%d sslmode=%s", host, user, password, dbname, port, sslmode)

	ctx := context.Background()
	pool, err := pgxpool.New(ctx, url)
	if err != nil {
		log.Fatalf("Failed to create connection pool: %v", err)
	}

	// Validate DB connectivity
	if err := pool.Ping(ctx); err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	return pool
}
