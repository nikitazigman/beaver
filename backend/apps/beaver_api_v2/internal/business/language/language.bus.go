package language

import (
	db "beaver-api/internal/db/language"
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

func (s *Service) RetrieveLanguages(ctx context.Context, offset int, size int) ([]Language, error) {
	qp := db.ListLanguagesParams{Offset: int32(offset), Limit: int32(size)}

	lds, err := s.q.ListLanguages(ctx, qp)
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

// TODO: should return ids
func (s *Service) CreateLanguages(ctx context.Context, ls []Language) error {
	ns := make([]pgtype.Text, len(ls))
	for i, l := range ls {
		ns[i] = pgtype.Text{String: l.Name, Valid: true}
	}
	var lErr error
	s.q.CreateLanguages(ctx, ns).Exec(func(i int, err error) {
		if err != nil {
			// TODO: check when error in the middle
			lErr = err
		}
	})

	return lErr
}

func (s *Service) DeleteLanguages(ctx context.Context, ids []uuid.UUID) error {
	var lErr error
	s.q.DeleteLanguages(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			lErr = err
		}
	})

	return lErr
}
