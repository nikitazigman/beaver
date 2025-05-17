package language

import (
	"beaver-api/internal/business/language"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *language.Service) {
	ctrl := new(s)

	r.Get("/languages/", ctrl.List)
}
