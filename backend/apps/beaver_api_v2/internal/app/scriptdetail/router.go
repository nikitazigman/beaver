package scriptdetail

import (
	biz "beaver-api/internal/business/scriptdetail"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *biz.Service) {
	ctrl := NewController(s)

	r.Get("/script", ctrl.GetRandomScript)
}
