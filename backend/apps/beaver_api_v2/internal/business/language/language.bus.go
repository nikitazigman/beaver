package language

import (
	"beaver-api/internal/db/language"
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct{}

func New() *Service {
	return &Service{}
}

func (s *Service) RetrieveLanguages(ctx context.Context, db *pgx.Conn, offset int, size int) ([]Language, error) {
	repo := language.New(db)
	qp := language.ListLanguagesParams{Offset: int32(offset), Limit: int32(size)}

	lds, err := repo.ListLanguages(ctx, qp)
	if err != nil {
		return nil, err
	}

	lbs := make([]Language, len(lds))
	for i, ld := range lds {
		bt, err := toLanguageBus(ld)
		if err != nil {
			return nil, err
		}
		lbs[i] = bt
	}

	return lbs, nil
}

func (s *Service) UpsertLanguages(ctx context.Context, db *pgx.Conn, ls []Language) error {
	repo := language.New(db)

	ns := make([]pgtype.Text, len(ls))
	for i, l := range ls {
		ns[i] = pgtype.Text{String: l.Name, Valid: true}
	}
	var lErr error
	repo.UpsertLanguages(ctx, ns).Exec(func(i int, err error) {
		if err != nil {
			// TODO: check when error in the middle
			lErr = err
		}
	})

	return lErr
}

func (s *Service) DeleteLanguages(ctx context.Context, db *pgx.Conn, ids []uuid.UUID) error {
	repo := language.New(db)

	var lErr error
	repo.DeleteLanguages(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			lErr = err
		}
	})

	return lErr
}
