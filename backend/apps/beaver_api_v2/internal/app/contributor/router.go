package contributor

import (
	biz "beaver-api/internal/business/contributor"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *biz.Service) {
	ctrl := newContribController(s)

	r.Get("/contributors", ctrl.ListContributors)
}
