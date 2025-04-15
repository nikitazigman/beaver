package contributorapp

import (
	"beaver-api/internal/business/contributorbus"

	"github.com/go-chi/chi/v5"
)

func New(r chi.Router ,cs *contributorbus.ContribService){
	contribCtrl := newContribController(cs)

	r.Get("/contributors", contribCtrl.ListContributors)
}
