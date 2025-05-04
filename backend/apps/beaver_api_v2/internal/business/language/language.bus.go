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

func (s *Service) Retrieve(ctx context.Context, db *pgx.Conn, offset int, size int) ([]Language, error) {
	repo := language.New(db)
	qp := language.ListParams{Offset: int32(offset), Limit: int32(size)}

	lds, err := repo.List(ctx, qp)
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

func (s *Service) Upsert(ctx context.Context, db *pgx.Conn, name string) (uuid.UUID, error) {
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

func (s *Service) Delete(ctx context.Context, db *pgx.Conn, ids []uuid.UUID) error {
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
