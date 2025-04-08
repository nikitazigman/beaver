package business

import (
	"github.com/google/uuid"
)


type Script struct {
	ID uuid.UUID
	Title string
	Code string
	LinkToProject string
	LanguageID uuid.UUID
	Language Language
	Tags []Tag
	Contributors []Contributor
}
