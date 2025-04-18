package tag

import biz "beaver-api/internal/business/tag"

type GetTagDTO struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type GetTagsDTO struct {
	Offset int `json:"offset"`
	Size   int `json:"size"`
	Value  []GetTagDTO
}

func BusTagsToGetTagsDTO(tag []biz.Tag, offset int, size int) GetTagsDTO {
	v := make([]GetTagDTO, len(tag))
	for i, bt := range tag {
		v[i] = GetTagDTO{
			ID:   bt.ID.String(),
			Name: bt.Name,
		}
	}

	return GetTagsDTO{
		Offset: offset,
		Size:   size,
		Value:  v,
	}
}
