package language

import (
	"beaver-api/internal/db/language"
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
	return &Service{
		PageSize: pageSize,
	}
}

func (s *Service) Retrieve(ctx context.Context, db pgx.Tx, page int) (LanguagePage, error) {
	repo := language.New(db)
	qp := language.ListParams{Offset: int32(page * s.PageSize), Limit: int32(s.PageSize)}

	langsDB, err := repo.List(ctx, qp)
	if err != nil {
		return LanguagePage{}, err
	}

	langs := make([]Language, len(langsDB))
	for i, ld := range langsDB {
		bt, err := toLanguageBus(ld)
		if err != nil {
			return LanguagePage{}, err
		}
		langs[i] = bt
	}
	langCount, err := repo.Count(ctx)
	if err != nil {
		return LanguagePage{}, err
	}

	count := int(langCount)

	nextPage := ""
	if count > s.PageSize {
		nextPage = fmt.Sprintf("/api/v1/languages/?page=%d", page+1)
	}

	previousPage := ""
	if page > 0 {
		previousPage = fmt.Sprintf("/api/v1/languages/?page=%d", page-1)
	}
	res := LanguagePage{
		Count:    count,
		Next:     nextPage,
		Previous: previousPage,
		Results:  langs,
	}
	return res, nil
}

func (s *Service) Upsert(ctx context.Context, db pgx.Tx, name string) (uuid.UUID, error) {
	repo := language.New(db)
	var uuid uuid.UUID
	dbName := pgtype.Text{String: name, Valid: true}
	if err := repo.Upsert(ctx, dbName); err != nil {
		return uuid, err
	}

	uuid, err := repo.GetID(ctx, dbName)
	if err != nil {
		return uuid, err
	}

	return uuid, nil
}

func (s *Service) Delete(ctx context.Context, db pgx.Tx, ids []uuid.UUID) error {
	repo := language.New(db)

	var lErr error
	repo.Delete(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			lErr = err
		}
	})

	return lErr
}
