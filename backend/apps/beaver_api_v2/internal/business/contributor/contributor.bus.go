package contributor

import (
	db "beaver-api/internal/db/contributor"

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

func (s *Service) RetrieveContributors(ctx context.Context, offset int, size int) ([]Contributor, error) {
	qp := db.ListContributorsParams{Offset: int32(offset), Limit: int32(size)}

	cds, err := s.q.ListContributors(ctx, qp)
	if err != nil {
		return nil, err
	}

	cbs := make([]Contributor, len(cds))
	for i, cd := range cds {
		cb, err := toBusContrib(cd)
		if err != nil {
			return nil, err
		}
		cbs[i] = cb
	}

	return cbs, nil
}

// TODO: should return ids
func (s *Service) CreateContributors(ctx context.Context, cs []Contributor) error {
	qp := make([]db.CreateContributorsParams, len(cs))
	for i, c := range cs {
		qp[i] = db.CreateContributorsParams{
			Name:         pgtype.Text{String: c.Name, Valid: true},
			LastName:     pgtype.Text{String: c.LastName, Valid: true},
			EmailAddress: pgtype.Text{String: c.EmailAddress, Valid: true},
		}
	}

	var cErr error
	s.q.CreateContributors(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			// TODO: check when error in the middle
			cErr = err
		}
	})

	return cErr
}
func (s *Service) DeleteContributors(ctx context.Context, ids []uuid.UUID) error {
	var cErr error
	s.q.DeleteContributors(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			cErr = err
		}
	})

	return cErr
}
