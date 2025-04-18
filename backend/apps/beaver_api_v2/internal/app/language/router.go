package language

import (
	biz "beaver-api/internal/business/language"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *biz.Service) {
	ctrl := newController(s)

	r.Get("/languages", ctrl.ListLangs)
}
