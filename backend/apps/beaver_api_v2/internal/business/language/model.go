package language

import (
	db "beaver-api/internal/db/language"
	"errors"

	"github.com/google/uuid"
)

type Language struct {
	ID   uuid.UUID
	Name string
}

func toLanguageBus(ld db.Language) (Language, error) {
	if !ld.Name.Valid {
		return Language{}, errors.New("ID or Name of language is not Valid")
	}

	l := Language{
		ID:   ld.ID,
		Name: ld.Name.String,
	}
	return l, nil
}
