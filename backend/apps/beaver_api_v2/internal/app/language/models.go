package language

import "beaver-api/internal/business/language"

type Language struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type GetLangsDTO struct {
	Count    int        `json:"count"`
	Next     string     `json:"next"`
	Previous string     `json:"previous"`
	Results  []Language `json:"results"`
}

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
