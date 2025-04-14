package tagapp

import (
	"beaver-api/internal/business/tagbus"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router ,ts *tagbus.TagService){
	tagApi := newTagController(ts)

	r.Get("/tags", tagApi.ListTags)
}
