package app

import "beaver-api/internal/business"

type GetTagDTO struct {
	ID string `json:"id"`
	Name string `json:"name"`
}

type GetTagsDTO struct {
	Offset int `json:"offset"`
	Size int `json:"size"`
	Value []GetTagDTO
}


func BusTagsToGetTagsDTO(bts []business.Tag, offset int, size int)GetTagsDTO{
	v := make([]GetTagDTO, len(bts))
	for i, bt :=range bts{
		v[i] = GetTagDTO{
			ID: bt.ID.String(),
			Name: bt.Name,
		}
	}

	return GetTagsDTO{
		Offset: offset,
		Size: size,
		Value: v,
	}
}
