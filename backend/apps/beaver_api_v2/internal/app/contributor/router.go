package contributor

import (
	"beaver-api/internal/business/contributor"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *contributor.Service) {
	ctrl := new(s)

	r.Get("/contributors/", ctrl.List)
}
