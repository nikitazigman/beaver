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

func (ts *Service) Retrieve(ctx context.Context, db *pgx.Conn, offset int, size int) ([]Tag, error) {
	repo := tag.New(db)

	qp := tag.ListParams{Offset: int32(offset), Limit: int32(size)}

	pgTags, err := repo.List(ctx, qp)
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

func (ts *Service) GetOrCreate(ctx context.Context, db *pgx.Conn, name string) (uuid.UUID, error) {
	repo := tag.New(db)
	tagName := pgtype.Text{String: name, Valid: true}

	var uuid uuid.UUID

	if err := repo.Upsert(ctx, tagName); err != nil {
		return uuid, err
	}

	uuid, err := repo.GetID(ctx, tagName)
	if err != nil {
		return uuid, err
	}

	return uuid, nil
}

func (ts *Service) Delete(ctx context.Context, db *pgx.Conn, ids []uuid.UUID) error {
	repo := tag.New(db)

	var tagErr error
	repo.Delete(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			tagErr = err
		}
	})

	return tagErr
}
