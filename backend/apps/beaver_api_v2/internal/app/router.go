package app

import (
	"beaver-api/internal/business"

	"github.com/go-chi/chi/v5"
)

func New(ts *business.TagService) *chi.Mux {
	r := chi.NewRouter()

	r.Route("/v1", func(r chi.Router) {
		tagApi := newTagController(ts)
		r.Get("/tags", tagApi.ListTags)
	})

	return r
}
