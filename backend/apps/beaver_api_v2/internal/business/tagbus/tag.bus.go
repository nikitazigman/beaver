package tagbus

import (
	"beaver-api/internal/storage/tagdb"
	"context"

	"github.com/jackc/pgx/v5/pgtype"
)

type TagService struct {
	repository *tagdb.Queries
}

func NewTagService(r *tagdb.Queries)*TagService{
	return &TagService{
		repository: r,
	}
}

func (ts *TagService)RetrieveTags(ctx context.Context, offset int, size int)([]Tag, error){
	qp := tagdb.ListTagsParams{Offset: int32(offset),Limit: int32(size)}

	pgTags, err := ts.repository.ListTags(ctx, qp)
	if err != nil{
		return nil, err
	}

	busTags := make([]Tag, len(pgTags))
	for i, pgTag := range pgTags {
		bt, err := toBusTag(pgTag)
		if err !=nil {
			return nil, err
		}
		busTags[i] = bt
	}

	return busTags, nil
}

func (ts *TagService)CreateTags(ctx context.Context, tags []Tag)([]Tag, error){
	names := make([]pgtype.Text, len(tags))
	for i, tag := range tags{
		names[i] = pgtype.Text{String: tag.Name, Valid: true}
	}

	var tagErr error

	ts.repository.CreateTags(ctx, names).Exec(func(i int, err error){
		if err != nil{
			// todo: log error here
			tagErr = err
			return
		}
	})

	if tagErr != nil{
		return nil, tagErr
	}

	return tags, nil
}
