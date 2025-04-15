package contributorapp

import (
	"beaver-api/internal/business/contributorbus"
	"encoding/json"
	"net/http"
	"strconv"
)

type ContribController struct {
	service *contributorbus.ContribService
}

func newContribController(cs *contributorbus.ContribService) *ContribController{
	return &ContribController{
		service: cs,
	}
}

func (cs *ContribController)ListContributors(w http.ResponseWriter, r *http.Request) {
	offset := 0
	size := 10
	var err error

	if o := r.URL.Query().Get("offset"); o != "" {
		offset, err = strconv.Atoi(o)
		if err!=nil {
			return
		}
	}
	if s := r.URL.Query().Get("size"); s != "" {
		size, err = strconv.Atoi(s)
		if err!=nil {
			return
		}
	}
	cbs, err := cs.service.RetrieveContributors(r.Context(), offset, size)
	if err!=nil {
		return
	}

	gcdto := contribBusToGetContribsDTO(cbs, offset, size)
	if err := json.NewEncoder(w).Encode(gcdto); err != nil {
		return
	}
}
