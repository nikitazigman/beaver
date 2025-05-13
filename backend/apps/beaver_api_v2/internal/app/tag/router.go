package tag

import (
	biz "beaver-api/internal/business/tag"

	"github.com/go-chi/chi/v5"
	"github.com/jackc/pgx/v5"
	"go.uber.org/zap"
)

func New(r chi.Router, s *biz.Service, db *pgx.Conn, logger *zap.SugaredLogger) {
	ctrl := new(s, db)

	r.Get("/tags/", ctrl.List)
}
