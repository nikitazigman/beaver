package tag

import (
	"beaver-api/internal/business/tag"
	"beaver-api/utils/middleware"
	"encoding/json"
	"net/http"
	"strconv"
)

type Controller struct {
	s *tag.Service
}

func new(s *tag.Service) *Controller {
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
	tagPage, err := c.s.Retrieve(r.Context(), tx, page)
	if err != nil {
		w.WriteHeader(500)
	}

	t := BusTagsToGetTagsDTO(tagPage)
	if err := json.NewEncoder(w).Encode(t); err != nil {
		return
	}
}
