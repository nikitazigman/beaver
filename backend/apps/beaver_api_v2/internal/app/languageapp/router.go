package languageapp

import (
	"beaver-api/internal/business/languagebus"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router ,ts *languagebus.LangService){
	langCtrl := newTagController(ts)

	r.Get("/languages", langCtrl.ListLangs)
}
