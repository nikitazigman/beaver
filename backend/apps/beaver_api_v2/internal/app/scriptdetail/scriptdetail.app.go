package scriptdetail

import (
	"beaver-api/internal/business/scriptdetail"
	"beaver-api/utils/middleware"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/google/uuid"
)

type Controller struct {
	s *scriptdetail.Service
}

func new(s *scriptdetail.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) GetRandomScript(w http.ResponseWriter, r *http.Request) {
	tx := middleware.GetTransactionFromContext(r.Context())
	script, err := c.s.GetRandomScriptDetail(r.Context(), tx, nil, nil, uuid.UUID{})

	if err != nil {
		fmt.Println(err)
	}
	dto := toDTO(script)

	if err := json.NewEncoder(w).Encode(dto); err != nil {
		return
	}
}
