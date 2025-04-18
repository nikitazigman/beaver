package tag

import (
	biz "beaver-api/internal/business/tag"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *biz.Service) {
	ctrl := newTagController(s)

	r.Get("/tags", ctrl.ListTags)
}
