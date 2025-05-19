package loader

import (
	"beaver-api/internal/business/contributor"
	"time"
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

type loaderScript struct {
	title         string
	code          string
	linkToProject string
	contributors  []string
	tags          []string
	language      string
}

type EntitiesToLoad struct {
	UniqueTags     []string
	UniqueLangs    []string
	UniqueContribs []contributor.UpsertContributor
	UniqueScripts  []loaderScript
}

func toEntitiesToLoad(scripts []Script, timestamp time.Time) EntitiesToLoad {
	uTags := NewUnique[string, string]()
	uLangs := NewUnique[string, string]()
	uContribs := NewUnique[string, contributor.UpsertContributor]()
	uScripts := NewUnique[string, loaderScript]()

	for _, s := range scripts {
		ctrb := make([]string, 0, len(s.Contributors))
		for _, c := range s.Contributors {
			ctrb = append(ctrb, c.EmailAddress)
		}
		uScripts.Insert(s.Title, loaderScript{
			title:         s.Title,
			code:          s.Code,
			linkToProject: s.LinkToProject,
			language:      s.Language,
			tags:          s.Tags,
			contributors:  ctrb,
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
