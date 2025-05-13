package main

import (
	contributorApp "beaver-api/internal/app/contributor"
	languageApp "beaver-api/internal/app/language"
	loaderApp "beaver-api/internal/app/loader"
	scriptDetailApp "beaver-api/internal/app/scriptdetail"
	tagApp "beaver-api/internal/app/tag"
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/loader"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/scriptdetail"
	"beaver-api/internal/business/tag"
	"beaver-api/utils/logger"
	beaverMiddleware "beaver-api/utils/middleware"

	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
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

	logger := logger.New(true)
	defer logger.Sync()

	url := fmt.Sprintf(fmtDBString, host, user, password, dbname, port)
	conn, err := pgx.Connect(context.Background(), url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())

	tagService := tag.New(10)
	langService := language.New(10)
	contribService := contributor.New()
	scriptDetailService := scriptdetail.New()
	scriptService := script.New()
	loaderService := loader.New(scriptService, tagService, contribService, langService)

	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(beaverMiddleware.LoggerMiddleware(logger))
	r.Use(middleware.Recoverer)
	r.Route("/api/v1", func(r chi.Router) {
		tagApp.New(r, tagService, conn, logger)
		languageApp.New(r, langService, conn, logger)
		contributorApp.New(r, contribService, conn, logger)
		scriptDetailApp.New(r, scriptDetailService, conn, logger)
		loaderApp.New(r, loaderService, conn, logger)
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
