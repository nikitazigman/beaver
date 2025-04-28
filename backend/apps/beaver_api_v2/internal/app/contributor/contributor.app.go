package contributor

import (
	biz "beaver-api/internal/business/contributor"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/jackc/pgx/v5"
)

type ContribController struct {
	s  *biz.Service
	db *pgx.Conn
}

func new(s *biz.Service, db *pgx.Conn) *ContribController {
	return &ContribController{
		s:  s,
		db: db,
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
	cbs, err := c.s.RetrieveContributors(r.Context(), c.db, offset, size)
	if err != nil {
		return
	}

	cas := contribBusToGetContribsDTO(cbs, offset, size)
	if err := json.NewEncoder(w).Encode(cas); err != nil {
		return
	}
}
