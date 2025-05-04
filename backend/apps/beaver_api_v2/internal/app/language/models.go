package language

import biz "beaver-api/internal/business/language"

type GetLangDTO struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type GetLangsDTO struct {
	Offset int `json:"offset"`
	Size   int `json:"size"`
	Value  []GetLangDTO
}

func langBusToGetLangsDTO(bls []biz.Language, offset int, size int) GetLangsDTO {
	v := make([]GetLangDTO, len(bls))
	for i, bt := range bls {
		v[i] = GetLangDTO{
			ID:   bt.ID.String(),
			Name: bt.Name,
		}
	}

	return GetLangsDTO{
		Offset: offset,
		Size:   size,
		Value:  v,
	}
}
