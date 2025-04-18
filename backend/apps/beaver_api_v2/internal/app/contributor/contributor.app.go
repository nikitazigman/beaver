package contributor

import (
	biz "beaver-api/internal/business/contributor"
	"encoding/json"
	"net/http"
	"strconv"
)

type ContribController struct {
	s *biz.Service
}

func newContribController(s *biz.Service) *ContribController {
	return &ContribController{
		s: s,
	}
}

func (c *ContribController) ListContributors(w http.ResponseWriter, r *http.Request) {
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
	cbs, err := c.s.RetrieveContributors(r.Context(), offset, size)
	if err != nil {
		return
	}

	cas := contribBusToGetContribsDTO(cbs, offset, size)
	if err := json.NewEncoder(w).Encode(cas); err != nil {
		return
	}
}
