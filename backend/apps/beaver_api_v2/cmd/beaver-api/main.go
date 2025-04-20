package main

import (
	contrapp "beaver-api/internal/app/contributor"
	langapp "beaver-api/internal/app/language"
	scriptdetailapp "beaver-api/internal/app/scriptdetail"
	tagapp "beaver-api/internal/app/tag"
	contrbiz "beaver-api/internal/business/contributor"
	langbiz "beaver-api/internal/business/language"
	scriptdetailbiz "beaver-api/internal/business/scriptdetail"
	tagbiz "beaver-api/internal/business/tag"

	contrdb "beaver-api/internal/db/contributor"
	langdb "beaver-api/internal/db/language"
	scriptdetaildb "beaver-api/internal/db/scriptdetail"
	tagdb "beaver-api/internal/db/tag"

	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/jackc/pgx/v5"
)

const (
	fmtDBString = "host=%s user=%s password=%s dbname=%s port=%d sslmode=disable"
	host        = "localhost"
	user        = "beaver_api"
	password    = "beaver_api"
	dbname      = "beaver_api_db"
	port        = 5432
)

func main() {
	url := fmt.Sprintf(fmtDBString, host, user, password, dbname, port)

	conn, err := pgx.Connect(context.Background(), url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())

	r := chi.NewRouter()
	r.Route("/v1", func(r chi.Router) {
		tagDB := tagdb.New(conn)
		tagService := tagbiz.NewService(tagDB)
		langDB := langdb.New(conn)
		langService := langbiz.NewService(langDB)
		contribDB := contrdb.New(conn)
		contribService := contrbiz.NewService(contribDB)
		scriptDB := scriptdetaildb.New(conn)
		scriptService := scriptdetailbiz.New(scriptDB)
		tagapp.New(r, tagService)
		langapp.New(r, langService)
		contrapp.New(r, contribService)
		scriptdetailapp.New(r, scriptService)
	})

	s := &http.Server{
		Addr:    fmt.Sprintf(":%d", 8000),
		Handler: r,
	}

	log.Println("Starting server " + s.Addr)
	if err := s.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatal("Server startup failed")
	}
}
