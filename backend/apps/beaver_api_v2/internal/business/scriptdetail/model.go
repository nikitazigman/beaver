package scriptdetail

import (
	db "beaver-api/internal/db/scriptdetail"
	"time"

	"github.com/google/uuid"
)

type Language struct {
	ID   uuid.UUID
	Name string
}

type Tag struct {
	ID   uuid.UUID
	Name string
}

type Contributor struct {
	ID           uuid.UUID
	Name         string
	LastName     string
	EmailAddress string
}

type ScriptDetail struct {
	ID            uuid.UUID
	Title         string
	Code          string
	LinkToProject string
	Language      Language
	Tags          []Tag
	Contributors  []Contributor
	CreatedAt     time.Time
	UpdatedAt     time.Time
}

func toBus(scripts []db.ScriptsDetail) ScriptDetail {
	tagsMap := make(map[uuid.UUID]Tag)
	contribsMap := make(map[uuid.UUID]Contributor)

	for _, script := range scripts {
		tagsMap[script.TagID] = Tag{ID: script.TagID, Name: script.TagName.String}
		contribsMap[script.ContributorID] = Contributor{
			ID:           script.ContributorID,
			Name:         script.ContributorName.String,
			LastName:     script.ContributorLastName.String,
			EmailAddress: script.ContributorEmailAddress.String,
		}
	}

	tags := make([]Tag, 0, len(tagsMap))
	for _, tag := range tagsMap {
		tags = append(tags, tag)
	}

	contribs := make([]Contributor, 0, len(contribsMap))
	for _, contrib := range contribsMap {
		contribs = append(contribs, contrib)
	}

	dbScript := scripts[0]
	Script := ScriptDetail{
		ID:            dbScript.ScriptID,
		Title:         dbScript.ScriptTitle.String,
		Code:          dbScript.ScriptCode.String,
		LinkToProject: dbScript.ScriptLinkToProject.String,
		CreatedAt:     dbScript.ScriptCreatedAt.Time,
		UpdatedAt:     dbScript.ScriptUpdatedAt.Time,
		Language:      Language{ID: dbScript.LanguageID, Name: dbScript.LanguageName.String},
		Tags:          tags,
		Contributors:  contribs,
	}

	return Script
}
