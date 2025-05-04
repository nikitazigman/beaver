package loader

import (
	biz "beaver-api/internal/business/loader"

	"github.com/go-chi/chi/v5"
	"github.com/jackc/pgx/v5"
)

func New(r chi.Router, s *biz.Service, db *pgx.Conn) {
	ctrl := new(s, db)

	r.Post("/loader/scripts", ctrl.LoadScripts)
}
