package busscript

import (
	"github.com/google/uuid"
)

type Language struct {
	ID uuid.UUID
	Name string
}

type Contributor struct {
	ID uuid.UUID
	Name string
	LastName string
	EmailAddress string
}


type Tag struct {
	ID   uuid.UUID
	Name string
}

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
