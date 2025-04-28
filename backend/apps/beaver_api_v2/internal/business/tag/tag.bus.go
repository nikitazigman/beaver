package tag

import (
	"beaver-api/internal/db/tag"
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct{}

func New() *Service {
	return &Service{}
}

func (ts *Service) RetrieveTags(ctx context.Context, db *pgx.Conn, offset int, size int) ([]Tag, error) {
	repo := tag.New(db)

	qp := tag.ListTagsParams{Offset: int32(offset), Limit: int32(size)}

	pgTags, err := repo.ListTags(ctx, qp)
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

func (ts *Service) CreateTags(ctx context.Context, db *pgx.Conn, tags []Tag) error {
	repo := tag.New(db)

	names := make([]pgtype.Text, len(tags))
	for i, tag := range tags {
		names[i] = pgtype.Text{String: tag.Name, Valid: true}
	}

	var tagErr error
	repo.UpsertTags(ctx, names).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			tagErr = err
		}
	})

	return tagErr
}

func (ts *Service) DeleteTags(ctx context.Context, db *pgx.Conn, ids []uuid.UUID) error {
	repo := tag.New(db)

	var tagErr error
	repo.DeleteTags(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			tagErr = err
		}
	})

	return tagErr
}
