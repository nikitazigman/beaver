package tag

import (
	"beaver-api/internal/db/tag"
	"context"
	"fmt"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct {
	PageSize int
}

func New(pageSize int) *Service {
	return &Service{PageSize: pageSize}
}

func (s *Service) Retrieve(ctx context.Context, db *pgx.Conn, page int) (TagPage, error) {
	repo := tag.New(db)

	qp := tag.ListParams{Offset: int32(page * s.PageSize), Limit: int32(s.PageSize)}

	pgTags, err := repo.List(ctx, qp)
	if err != nil {
		return TagPage{}, err
	}

	busTags := make([]Tag, len(pgTags))
	for i, pgTag := range pgTags {
		bt, err := toBusTag(pgTag)
		if err != nil {
			return TagPage{}, err
		}
		busTags[i] = bt
	}

	tagCount, err := repo.Count(ctx)
	count := int(tagCount)
	if err != nil {
		return TagPage{}, err
	}

	nextPage := ""
	if count > s.PageSize {
		nextPage = fmt.Sprintf("/api/v1/tags/?page=%d", page+1)
	}

	previousPage := ""
	if page > 0 {
		previousPage = fmt.Sprintf("/api/v1/tags/?page=%d", page-1)
	}

	result := TagPage{
		Count:    int(tagCount),
		Next:     nextPage,
		Previous: previousPage,
		Results:  busTags,
	}
	return result, nil
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
