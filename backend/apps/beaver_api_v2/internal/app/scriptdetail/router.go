package scriptdetail

import (
	biz "beaver-api/internal/business/scriptdetail"

	"github.com/go-chi/chi/v5"
	"github.com/jackc/pgx/v5"
	"go.uber.org/zap"
)

func New(r chi.Router, s *biz.Service, db *pgx.Conn, logger *zap.SugaredLogger) {
	ctrl := new(s, db)

	r.Get("/code_documents/code_document/", ctrl.GetRandomScript)
}
