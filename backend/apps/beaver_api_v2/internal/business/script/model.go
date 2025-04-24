package script

import (
	"time"

	"github.com/google/uuid"
)

type ContributorScript struct {
	ID            uuid.UUID
	ContributorID uuid.UUID
	ScriptID      uuid.UUID
}

type TagScript struct {
	ID       uuid.UUID
	TagID    uuid.UUID
	ScriptID uuid.UUID
}

type Script struct {
	ID            uuid.UUID
	Title         string
	Code          string
	LinkToProject string
	LanguageID    uuid.UUID
	CreatedAt     time.Time
}
