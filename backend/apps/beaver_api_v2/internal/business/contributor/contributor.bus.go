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

func (s *Service) Retrieve(ctx context.Context, db pgx.Tx, offset int, size int) ([]Contributor, error) {
	repo := contributor.New(db)
	qp := contributor.ListParams{Offset: int32(offset), Limit: int32(size)}

	cds, err := repo.List(ctx, qp)
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

func (s *Service) UpsertContributors(ctx context.Context, db pgx.Tx, contrib UpsertContributor) (uuid.UUID, error) {
	repo := contributor.New(db)
	var uuid uuid.UUID

	dbContrib := contributor.UpsertParams{
		Name:         pgtype.Text{String: contrib.Name, Valid: true},
		LastName:     pgtype.Text{String: contrib.LastName, Valid: true},
		EmailAddress: pgtype.Text{String: contrib.EmailAddress, Valid: true},
	}

	if err := repo.Upsert(ctx, dbContrib); err != nil {
		return uuid, err
	}

	uuid, err := repo.GetID(ctx, dbContrib.EmailAddress)
	if err != nil {
		return uuid, err
	}

	return uuid, nil
}

func (s *Service) KeepOnly(ctx context.Context, db pgx.Tx, ids []uuid.UUID) error {
	repo := contributor.New(db)
	if err := repo.KeepOnly(ctx, ids); err != nil {
		return err
	}
	return nil
}
