package loader

import (
	"beaver-api/internal/business/loader"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *loader.Service) {
	ctrl := new(s)
	r.Post("/bulk_update/", ctrl.LoadScripts)
	r.Post("/bulk_delete/", ctrl.DeleteScripts)
}
