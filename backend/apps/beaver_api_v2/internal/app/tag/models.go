package tag

import "beaver-api/internal/business/tag"

type GetTagDTO struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type GetTagsDTO struct {
	Count    int         `json:"count"`
	Next     string      `json:"next"`
	Previous string      `json:"previous"`
	Results  []GetTagDTO `json:"results"`
}

func BusTagsToGetTagsDTO(tag tag.TagPage) GetTagsDTO {
	v := make([]GetTagDTO, len(tag.Results))
	for i, bt := range tag.Results {
		v[i] = GetTagDTO{
			ID:   bt.ID.String(),
			Name: bt.Name,
		}
	}

	return GetTagsDTO{
		Count:    tag.Count,
		Next:     tag.Next,
		Previous: tag.Previous,
		Results:  v,
	}
}
