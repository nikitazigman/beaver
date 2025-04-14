package languageapp

import (
	"beaver-api/internal/business/languagebus"
	"encoding/json"
	"net/http"
	"strconv"
)

type TagController struct {
	service *languagebus.LangService
}

func newTagController(ts *languagebus.LangService) *TagController{
	return &TagController{
		service: ts,
	}
}

func (tc *TagController)ListLangs(w http.ResponseWriter, r *http.Request) {
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
	bts, err := tc.service.RetrieveLanguages(r.Context(), offset, size)
	if err!=nil {
		return
	}

	dts := langBusToGetLangsDTO(bts, offset, size)
	if err := json.NewEncoder(w).Encode(dts); err != nil {
		return
	}
}
