package tag

import (
	biz "beaver-api/internal/business/tag"
	"encoding/json"
	"net/http"
	"strconv"
)

type Controller struct {
	s *biz.Service
}

func newTagController(s *biz.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) ListTags(w http.ResponseWriter, r *http.Request) {
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
	bt, err := c.s.RetrieveTags(r.Context(), offset, size)
	if err != nil {
		return
	}

	t := BusTagsToGetTagsDTO(bt, offset, size)
	if err := json.NewEncoder(w).Encode(t); err != nil {
		return
	}
}
