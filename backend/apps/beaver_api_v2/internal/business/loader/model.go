package loader

import (
	"beaver-api/internal/business/contributor"
	"beaver-api/internal/business/language"
	"beaver-api/internal/business/script"
	"beaver-api/internal/business/tag"
	"time"

	"github.com/google/uuid"
)

type Language struct {
	Name string
}

type Tag struct {
	Name string
}

type Contributor struct {
	Name         string
	LastName     string
	EmailAddress string
}

type ScriptDetail struct {
	Title         string
	Code          string
	LinkToProject string
	Language      Language
	Tags          []Tag
	Contributors  []Contributor
}

type Loader struct {
	tags          []tag.Tag
	contributors  []contributor.Contributor
	langs         []language.Language
	scripts       []script.Script
	tagScript     []script.TagScript
	contribScript []script.ContributorScript
}

func toEntities(scriptDetails []ScriptDetail, timestamp time.Time) Loader {
	tagMap := make(map[string]uuid.UUID)
	contributorMap := make(map[string]uuid.UUID)
	langMap := make(map[string]uuid.UUID)

	scripts := make([]script.Script, len(scriptDetails))
	tags := make([]tag.Tag, 0, len(scriptDetails))
	contributors := make([]contributor.Contributor, 0, len(scriptDetails))
	langs := make([]language.Language, 0, len(scriptDetails))
	tagScript := make([]script.TagScript, 0, len(scriptDetails))
	contribScript := make([]script.ContributorScript, 0, len(scriptDetails))

	var langID uuid.UUID
	var tagID uuid.UUID
	var contribID uuid.UUID
	var ok bool

	for i, s := range scriptDetails {
		langID, ok = langMap[s.Language.Name]
		if !ok {
			langID = uuid.New()
			langMap[s.Language.Name] = langID
			langs = append(langs, language.Language{ID: langID, Name: s.Language.Name})
		}

		scriptID := uuid.New()
		scripts[i] = script.Script{
			ID:            scriptID,
			Title:         s.Title,
			Code:          s.Code,
			LinkToProject: s.LinkToProject,
			CreatedAt:     timestamp,
			LanguageID:    langID,
		}

		for _, t := range s.Tags {
			tagID, ok = tagMap[t.Name]
			if !ok {
				tagID = uuid.New()
				tagMap[t.Name] = tagID
				tags = append(tags, tag.Tag{ID: tagID, Name: t.Name})
			}
			tagScript = append(tagScript, script.TagScript{ID: uuid.New(), TagID: tagID, ScriptID: scriptID})
		}
		for _, c := range s.Contributors {
			contribID, ok = contributorMap[c.EmailAddress]
			if !ok {
				contribID = uuid.New()
				contributorMap[c.EmailAddress] = contribID
				contributors = append(contributors, contributor.Contributor{
					ID:           contribID,
					Name:         c.Name,
					LastName:     c.LastName,
					EmailAddress: c.EmailAddress,
				})
			}
			contribScript = append(contribScript, script.ContributorScript{ID: uuid.New(), ScriptID: scriptID, ContributorID: contribID})
		}

	}
	return Loader{
		tags:          tags,
		contributors:  contributors,
		langs:         langs,
		scripts:       scripts,
		tagScript:     tagScript,
		contribScript: contribScript,
	}
}
