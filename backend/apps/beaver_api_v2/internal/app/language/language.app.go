package language

import (
	biz "beaver-api/internal/business/language"
	"beaver-api/utils/middleware"
	"encoding/json"
	"net/http"
	"strconv"
)

type Controller struct {
	s *biz.Service
}

func new(s *biz.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) List(w http.ResponseWriter, r *http.Request) {
	page := 0
	var err error

	if p := r.URL.Query().Get("page"); p != "" {
		page, err = strconv.Atoi(p)
		if err != nil {
			w.WriteHeader(500)
		}
	}
	tx := middleware.GetTransactionFromContext(r.Context())
	lbs, err := c.s.Retrieve(r.Context(), tx, page)
	if err != nil {
		return
	}

	langPage := langBusToGetLangsDTO(lbs)
	if err := json.NewEncoder(w).Encode(langPage); err != nil {
		return
	}
}
