package tag

import (
	db "beaver-api/internal/db/tag"
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct {
	q *db.Queries
}

func NewService(q *db.Queries) *Service {
	return &Service{
		q: q,
	}
}

func (ts *Service) RetrieveTags(ctx context.Context, offset int, size int) ([]Tag, error) {
	qp := db.ListTagsParams{Offset: int32(offset), Limit: int32(size)}

	pgTags, err := ts.q.ListTags(ctx, qp)
	if err != nil {
		return nil, err
	}

	busTags := make([]Tag, len(pgTags))
	for i, pgTag := range pgTags {
		bt, err := toBusTag(pgTag)
		if err != nil {
			return nil, err
		}
		busTags[i] = bt
	}

	return busTags, nil
}

// TODO: should return ids
func (ts *Service) CreateTags(ctx context.Context, tags []Tag) error {
	names := make([]pgtype.Text, len(tags))
	for i, tag := range tags {
		names[i] = pgtype.Text{String: tag.Name, Valid: true}
	}

	var tagErr error
	ts.q.CreateTags(ctx, names).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			tagErr = err
		}
	})

	return tagErr
}

func (ts *Service) DeleteTags(ctx context.Context, ids []uuid.UUID) error {
	var tagErr error
	ts.q.DeleteTags(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			tagErr = err
		}
	})

	return tagErr
}
