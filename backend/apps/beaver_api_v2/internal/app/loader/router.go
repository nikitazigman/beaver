package loader

import (
	biz "beaver-api/internal/business/loader"

	"github.com/go-chi/chi/v5"
	"github.com/jackc/pgx/v5"
	"go.uber.org/zap"
)

func New(r chi.Router, s *biz.Service, db *pgx.Conn, logger *zap.SugaredLogger) {
	ctrl := new(s, db)

	r.Post("/code_documents/bulk_update/", ctrl.LoadScripts)
}
