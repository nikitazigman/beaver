package loader

import (
	biz "beaver-api/internal/business/loader"
	"encoding/json"
	"fmt"
	"net/http"

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

func (c *Controller) LoadScripts(w http.ResponseWriter, r *http.Request) {
	dto := POSTLoadScriptsDTO{}

	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&dto)
	if err != nil {
		fmt.Println(err)
		return
	}
	sd, t, err := toScriptDetail(dto)

	err = c.s.LoadScripts(r.Context(), c.db, sd, t)
	if err != nil {
		fmt.Println(err)
	}
}
