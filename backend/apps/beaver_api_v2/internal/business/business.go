package business

import (
	"beaver-api/internal/storage"
	"context"
)

type TagService struct {
	repository *storage.Queries
}

func NewTagService(r *storage.Queries)*TagService{
	return &TagService{
		repository: r,
	}
}

func (ts *TagService)RetrieveTags(ctx context.Context, offset int, size int)([]Tag, error){
	qp := storage.ListTagsParams{Offset: int32(offset),Limit: int32(size)}

	pgTags, err := ts.repository.ListTags(ctx, qp)
	if err != nil{
		return nil, err
	}

	busTags := make([]Tag, len(pgTags))
	for i, pgTag := range pgTags {
		bt, err := ToBusTag(pgTag)
		if err !=nil {
			return nil, err
		}
		busTags[i] = bt
	}

	return busTags, nil
}
