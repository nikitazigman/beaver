package app

import (
	"beaver-api/internal/business"
	"encoding/json"
	"net/http"
	"strconv"
)

type TagController struct {
	service *business.TagService
}

func newTagController(ts *business.TagService) *TagController{
	return &TagController{
		service: ts,
	}
}

func (tc *TagController)ListTags(w http.ResponseWriter, r *http.Request) {
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
	bts, err := tc.service.RetrieveTags(r.Context(), offset, size)
	if err!=nil {
		return
	}

	dts := BusTagsToGetTagsDTO(bts, offset, size)
	if err := json.NewEncoder(w).Encode(dts); err != nil {
		return
	}
}
