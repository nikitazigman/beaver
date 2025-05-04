package script

import (
	"beaver-api/internal/db/script"
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct{}

func New() *Service {
	return &Service{}
}

func (s *Service) Upsert(ctx context.Context, db *pgx.Conn, upsertScript UpsertScript) (uuid.UUID, error) {
	repo := script.New(db)
	var uuid uuid.UUID
	qp := script.UpsertParams{
		Title:         pgtype.Text{String: upsertScript.Title, Valid: true},
		Code:          pgtype.Text{String: upsertScript.Code, Valid: true},
		LinkToProject: pgtype.Text{String: upsertScript.LinkToProject, Valid: true},
		LanguageID:    pgtype.UUID{Bytes: upsertScript.LanguageID, Valid: true},
	}
	if err := repo.Upsert(ctx, qp); err != nil {
		return uuid, err
	}

	uuid, err := repo.GetID(ctx, qp.Title)
	if err != nil {
		return uuid, err
	}

	return uuid, nil
}

func (s *Service) LinkTag(ctx context.Context, db *pgx.Conn, link TagScript) error {
	repo := script.New(db)
	qp := script.LinkTagParams{
		TagID:    pgtype.UUID{Bytes: link.TagID, Valid: true},
		ScriptID: pgtype.UUID{Bytes: link.ScriptID, Valid: true},
	}

	if err := repo.LinkTag(ctx, qp); err != nil {
		return err
	}

	return nil
}

func (s *Service) LinkContrib(ctx context.Context, db *pgx.Conn, link ContributorScript) error {
	repo := script.New(db)
	qp := script.LinkContribParams{
		ContributorID: pgtype.UUID{Bytes: link.ContributorID, Valid: true},
		ScriptID:      pgtype.UUID{Bytes: link.ScriptID, Valid: true},
	}

	if err := repo.LinkContrib(ctx, qp); err != nil {
		return err
	}

	return nil
}
