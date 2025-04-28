package contributor

import (
	"beaver-api/internal/db/contributor"

	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct{}

func New() *Service {
	return &Service{}
}

func (s *Service) RetrieveContributors(ctx context.Context, db *pgx.Conn, offset int, size int) ([]Contributor, error) {
	repo := contributor.New(db)
	qp := contributor.ListContributorsParams{Offset: int32(offset), Limit: int32(size)}

	cds, err := repo.ListContributors(ctx, qp)
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

func (s *Service) UpsertContributors(ctx context.Context, db *pgx.Conn, cs []Contributor) error {
	repo := contributor.New(db)

	qp := make([]contributor.UpsertContributorsParams, len(cs))
	for i, c := range cs {
		qp[i] = contributor.UpsertContributorsParams{
			Name:         pgtype.Text{String: c.Name, Valid: true},
			LastName:     pgtype.Text{String: c.LastName, Valid: true},
			EmailAddress: pgtype.Text{String: c.EmailAddress, Valid: true},
		}
	}

	var cErr error
	repo.UpsertContributors(ctx, qp).Exec(func(i int, err error) {
		if err != nil {
			// TODO: check when error in the middle
			cErr = err
		}
	})

	return cErr
}

func (s *Service) DeleteContributors(ctx context.Context, db *pgx.Conn, ids []uuid.UUID) error {
	repo := contributor.New(db)
	var cErr error
	repo.DeleteContributors(ctx, ids).Exec(func(i int, err error) {
		if err != nil {
			// TODO check when error in the middle
			cErr = err
		}
	})

	return cErr
}
