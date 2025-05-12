package tag

import (
	"beaver-api/internal/business/tag"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/jackc/pgx/v5"
)

type Controller struct {
	s  *tag.Service
	db *pgx.Conn
}

func new(s *tag.Service, db *pgx.Conn) *Controller {
	return &Controller{
		s:  s,
		db: db,
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

	tagPage, err := c.s.Retrieve(r.Context(), c.db, page)
	if err != nil {
		w.WriteHeader(500)
	}

	t := BusTagsToGetTagsDTO(tagPage)
	if err := json.NewEncoder(w).Encode(t); err != nil {
		return
	}
}
