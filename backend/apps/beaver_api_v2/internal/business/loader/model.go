package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/script"
	"time"

	"github.com/google/uuid"
)

type Contributor struct {
	Name         string
	LastName     string
	EmailAddress string
}

type Script struct {
	Title         string
	Code          string
	LinkToProject string
	Contributors  []Contributor
	Tags          []string
	Language      string
}

type EntitiesToLoad struct {
	UniqueTags     []string
	UniqueLangs    []string
	UniqueContribs []contributor.UpsertContributor
	UniqueScripts  []script.UpsertScript
}

func toEntitiesToLoad(scripts []Script, timestamp time.Time) EntitiesToLoad {
	uTags := NewUnique[string, string]()
	uLangs := NewUnique[string, string]()
	uContribs := NewUnique[string, contributor.UpsertContributor]()
	uScripts := NewUnique[string, script.UpsertScript]()

	for _, s := range scripts {
		uScripts.Insert(s.Title, script.UpsertScript{
			Title:         s.Title,
			Code:          s.Code,
			LinkToProject: s.LinkToProject,
			LanguageID:    uuid.UUID{},
		})

		uLangs.Insert(s.Language, s.Language)

		for _, t := range s.Tags {
			uTags.Insert(t, t)
		}

		for _, c := range s.Contributors {
			uContribs.Insert(c.EmailAddress, contributor.UpsertContributor{
				Name:         c.Name,
				LastName:     c.LastName,
				EmailAddress: c.EmailAddress,
			})
		}
	}

	return EntitiesToLoad{
		UniqueTags:     uTags.Get(),
		UniqueLangs:    uLangs.Get(),
		UniqueContribs: uContribs.Get(),
		UniqueScripts:  uScripts.Get(),
	}
}
