package tag

import (
	"beaver-api/internal/business/tag"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *tag.Service) {
	ctrl := new(s)

	r.Get("/tags/", ctrl.List)
}
