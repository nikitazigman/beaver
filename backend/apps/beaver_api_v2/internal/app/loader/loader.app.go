package loader

import (
	biz "beaver-api/internal/business/loader"
	"encoding/json"
	"fmt"
	"net/http"
)

type Controller struct {
	s *biz.Service
}

func NewController(s *biz.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) LoadScripts(w http.ResponseWriter, r *http.Request) {
	dto := POSTLoadScriptsDTO{}
	err := json.NewDecoder(r.Body).Decode(&dto)
	if err != nil {
		fmt.Println(err)
	}
	sd, t, err := toScriptDetail(dto)

	err = c.s.LoadScripts(r.Context(), sd, t)
	if err != nil {
		fmt.Println(err)
	}
}
