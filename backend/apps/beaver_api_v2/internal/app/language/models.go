package language

import (
	"beaver-api/internal/business/language"
	"beaver-api/utils/pagination"
)

type Language struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type GetLangsDTO pagination.Page[Language]

func langBusToGetLangsDTO(langPage language.LanguagePage) GetLangsDTO {
	langs := make([]Language, len(langPage.Results))
	for i, l := range langPage.Results {
		langs[i] = Language{
			ID:   l.ID.String(),
			Name: l.Name,
		}
	}

	return GetLangsDTO{
		Count:    langPage.Count,
		Next:     langPage.Next,
		Previous: langPage.Previous,
		Results:  langs,
	}
}
