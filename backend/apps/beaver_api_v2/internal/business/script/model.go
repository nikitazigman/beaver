package script

import (
	"time"

	"github.com/google/uuid"
)

type ContributorScript struct {
	ContributorID uuid.UUID
	ScriptID      uuid.UUID
}

type TagScript struct {
	TagID    uuid.UUID
	ScriptID uuid.UUID
}

type UpsertScript struct {
	Title         string
	Code          string
	LinkToProject string
	LanguageID    uuid.UUID
	CreatedAt     time.Time
}
