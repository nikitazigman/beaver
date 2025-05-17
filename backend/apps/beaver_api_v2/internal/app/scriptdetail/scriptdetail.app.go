package scriptdetail

import (
	"beaver-api/internal/business/scriptdetail"
	"beaver-api/utils/middleware"
	"encoding/json"
	"net/http"
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
	tags := r.URL.Query()["tags"]
	if len(tags) == 0 {
		tags = nil
	}

	langs := r.URL.Query()["languages"]
	if len(langs) == 0 {
		langs = nil
	}
	contribs := r.URL.Query()["contributors"]
	if len(contribs) == 0 {
		contribs = nil
	}

	tx := middleware.GetTransactionFromContext(r.Context())
	script, err := c.s.GetRandomScriptDetail(r.Context(), tx, tags, contribs, langs)

	if err != nil {
		w.WriteHeader(http.StatusNotFound)
		return
	}
	dto := toDTO(script)

	if err := json.NewEncoder(w).Encode(dto); err != nil {
		return
	}
}
