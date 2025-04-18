package language

import (
	biz "beaver-api/internal/business/language"
	"encoding/json"
	"net/http"
	"strconv"
)

type Controller struct {
	s *biz.Service
}

func newController(s *biz.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) ListLangs(w http.ResponseWriter, r *http.Request) {
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
	lbs, err := c.s.RetrieveLanguages(r.Context(), offset, size)
	if err != nil {
		return
	}

	las := langBusToGetLangsDTO(lbs, offset, size)
	if err := json.NewEncoder(w).Encode(las); err != nil {
		return
	}
}
