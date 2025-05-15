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
	"beaver-api/utils/db"
	"beaver-api/utils/logger"
	beaverMiddleware "beaver-api/utils/middleware"
	"time"

	"fmt"
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/kelseyhightower/envconfig"
	"go.uber.org/zap"
)

type Config struct {
	Debug    bool `envconfig:"DEBUG"`
	PageSize int  `envconfig:"PAGESIZE" default:"10"`

	ServerPort         int           `envconfig:"SERVER_PORT"`
	ServerTimeoutRead  time.Duration `envconfig:"SERVER_TIMEOUT_READ" default:"3s"`
	ServerTimeoutWrite time.Duration `envconfig:"SERVER_TIMEOUT_WRITE" default:"5s"`
	ServerTimeoutIdle  time.Duration `envconfig:"SERVER_TIMEOUT_IDLE" default:"5s"`

	DBHost string `envconfig:"DB_HOST"`
	DBPort int    `envconfig:"DB_PORT"`
	DBUser string `envconfig:"DB_USER"`
	DBPass string `envconfig:"DB_PASS"`
	DBName string `envconfig:"DB_NAME"`
}

func NewConfig() *Config {
	var c Config

	err := envconfig.Process("", &c)
	if err != nil {
		log.Fatal("Cannot read configuration. Check envs.")
	}

	return &c
}

func NewController(config *Config, pool *pgxpool.Pool, logger *zap.SugaredLogger) *chi.Mux {
	tagService := tag.New(config.PageSize)
	langService := language.New(config.PageSize)
	contribService := contributor.New()
	scriptDetailService := scriptdetail.New()
	scriptService := script.New()
	loaderService := loader.New(scriptService, tagService, contribService, langService)

	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(beaverMiddleware.LoggerMiddleware(logger))
	r.Use(beaverMiddleware.TransactionMiddleware(pool))
	r.Use(middleware.Recoverer)

	r.Route("/api/v1", func(r chi.Router) {
		tagApp.New(r, tagService)
		languageApp.New(r, langService)
		contributorApp.New(r, contribService)
		scriptDetailApp.New(r, scriptDetailService)
		loaderApp.New(r, loaderService)
	})
	return r
}

func main() {
	config := NewConfig()

	logger := logger.New(config.Debug)
	defer logger.Sync()

	pool := db.New(config.DBHost, config.DBUser, config.DBPass, config.DBName, config.DBPort)
	defer pool.Close()

	controller := NewController(config, pool, logger)

	s := &http.Server{
		Addr:         fmt.Sprintf(":%d", 8000),
		Handler:      controller,
		ReadTimeout:  config.ServerTimeoutRead,
		WriteTimeout: config.ServerTimeoutWrite,
		IdleTimeout:  config.ServerTimeoutIdle,
	}

	log.Println("Starting server " + s.Addr)
	if err := s.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatal("Server startup failed")
	}
}
