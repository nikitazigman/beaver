package scriptdetail

import (
	biz "beaver-api/internal/business/scriptdetail"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/google/uuid"
)

type Controller struct {
	s *biz.Service
}

func NewController(s *biz.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) GetRandomScript(w http.ResponseWriter, r *http.Request) {
	script, err := c.s.GetRandomScriptDetail(r.Context(), nil, nil, uuid.UUID{})
	if err != nil {
		fmt.Println(err)
	}
	dto := toDTO(script)
	if err := json.NewEncoder(w).Encode(dto); err != nil {
		return
	}
	w.WriteHeader(http.StatusCreated)
}
