package contributor

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/utils/middleware"
	"encoding/json"
	"net/http"
	"strconv"
)

type Controller struct {
	s *contributor.Service
}

func new(s *contributor.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) List(w http.ResponseWriter, r *http.Request) {
	offset := 0
	size := 10
	var err error

	if o := r.URL.Query().Get("offset"); o != "" {
		offset, err = strconv.Atoi(o)
		if err != nil {
			return
		}
	}
	if s := r.URL.Query().Get("size"); s != "" {
		size, err = strconv.Atoi(s)
		if err != nil {
			return
		}
	}

	tx := middleware.GetTransactionFromContext(r.Context())
	cbs, err := c.s.Retrieve(r.Context(), tx, offset, size)
	if err != nil {
		return
	}

	cas := contribBusToGetContribsDTO(cbs, offset, size)
	if err := json.NewEncoder(w).Encode(cas); err != nil {
		return
	}
}
