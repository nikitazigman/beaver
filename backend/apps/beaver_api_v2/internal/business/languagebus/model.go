package languagebus

import (
	"beaver-api/internal/storage/languagedb"
	"errors"

	"github.com/google/uuid"
)



type Language struct {
	ID uuid.UUID
	Name string
}

func toLanguageBus(lang languagedb.Language)(Language, error){
	if !(lang.ID.Valid || lang.Name.Valid){
		return Language{}, errors.New("ID or Name of language is not Valid")
	}

	langBus :=  Language{
		ID: uuid.UUID(lang.ID.Bytes),
		Name: lang.Name.String,
	}
	return langBus, nil
}
