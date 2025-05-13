package tag

import (
	"beaver-api/internal/business/tag"
	"beaver-api/utils/pagination"
)

type Tag struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type GetTagsDTO pagination.Page[Tag]

func BusTagsToGetTagsDTO(tag tag.TagPage) GetTagsDTO {
	v := make([]Tag, len(tag.Results))
	for i, bt := range tag.Results {
		v[i] = Tag{
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
