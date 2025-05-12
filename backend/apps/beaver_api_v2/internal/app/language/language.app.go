package language

import (
	biz "beaver-api/internal/business/language"
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
	page := 0
	var err error

	if p := r.URL.Query().Get("page"); p != "" {
		page, err = strconv.Atoi(p)
		if err != nil {
			w.WriteHeader(500)
		}
	}

	lbs, err := c.s.Retrieve(r.Context(), c.db, page)
	if err != nil {
		return
	}

	langPage := langBusToGetLangsDTO(lbs)
	if err := json.NewEncoder(w).Encode(langPage); err != nil {
		return
	}
}
