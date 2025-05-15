package scriptdetail

import (
	biz "beaver-api/internal/business/scriptdetail"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router, s *biz.Service) {
	ctrl := new(s)

	r.Get("/code_documents/code_document/", ctrl.GetRandomScript)
}
