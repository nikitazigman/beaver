package tag

import (
	biz "beaver-api/internal/business/tag"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/jackc/pgx/v5"
)

type Controller struct {
	s  *biz.Service
	db *pgx.Conn
}

func new(s *biz.Service, db *pgx.Conn) *Controller {
	return &Controller{
		s:  s,
		db: db,
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
	bt, err := c.s.Retrieve(r.Context(), c.db, offset, size)
	if err != nil {
		return
	}

	t := BusTagsToGetTagsDTO(bt, offset, size)
	if err := json.NewEncoder(w).Encode(t); err != nil {
		return
	}
}
