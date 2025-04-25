package loader

import (
	biz "beaver-api/internal/business/loader"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *biz.Service) {
	ctrl := NewController(s)

	r.Post("loader/scripts", ctrl.LoadScripts)
}
