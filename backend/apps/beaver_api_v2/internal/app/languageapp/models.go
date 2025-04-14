package languageapp

import "beaver-api/internal/business/languagebus"

type GetLangDTO struct {
	ID string `json:"id"`
	Name string `json:"name"`
}

type GetLangsDTO struct {
	Offset int `json:"offset"`
	Size int `json:"size"`
	Value []GetLangDTO
}


func langBusToGetLangsDTO(bts []languagebus.Language, offset int, size int)GetLangsDTO{
	v := make([]GetLangDTO, len(bts))
	for i, bt :=range bts{
		v[i] = GetLangDTO{
			ID: bt.ID.String(),
			Name: bt.Name,
		}
	}

	return GetLangsDTO{
		Offset: offset,
		Size: size,
		Value: v,
	}
}
