package scriptdetail

import (
	biz "beaver-api/internal/business/scriptdetail"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/google/uuid"
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

func (c *Controller) GetRandomScript(w http.ResponseWriter, r *http.Request) {
	script, err := c.s.GetRandomScriptDetail(r.Context(), c.db, nil, nil, uuid.UUID{})
	if err != nil {
		fmt.Println(err)
	}
	dto := toDTO(script)
	if err := json.NewEncoder(w).Encode(dto); err != nil {
		return
	}
}
