package loader

import (
	"beaver-api/internal/business/loader"
	"beaver-api/utils/middleware"
	"encoding/json"
	"fmt"
	"net/http"
)

type Controller struct {
	s *loader.Service
}

func new(s *loader.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) LoadScripts(w http.ResponseWriter, r *http.Request) {
	var dto []POSTUpdateScriptDTO

	fmt.Println("got scripts to update")
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&dto)
	if err != nil {
		fmt.Println(err)
		return
	}
	scriptDetail, t, err := toScriptDetail(dto)
	if err != nil {
		fmt.Println(err)
		return
	}
	tx := middleware.GetTransactionFromContext(r.Context())
	err = c.s.LoadScripts(r.Context(), tx, scriptDetail, t)
	if err != nil {
		fmt.Println(err)
	}
}
