package script

import (
	"beaver-api/internal/db/script"
	"context"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

type Service struct{}

func New() *Service {
	return &Service{}
}

func (s *Service) Upsert(ctx context.Context, db pgx.Tx, upsertScript UpsertScript) (uuid.UUID, error) {
	repo := script.New(db)
	var uuid uuid.UUID
	qp := script.UpsertParams{
		Title:         pgtype.Text{String: upsertScript.Title, Valid: true},
		Code:          pgtype.Text{String: upsertScript.Code, Valid: true},
		LinkToProject: pgtype.Text{String: upsertScript.LinkToProject, Valid: true},
		LanguageID:    pgtype.UUID{Bytes: upsertScript.LanguageID, Valid: true},
		CreatedAt:     pgtype.Timestamptz{Time: upsertScript.CreatedAt, Valid: true},
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

func (s *Service) LinkTag(ctx context.Context, db pgx.Tx, link TagScript) error {
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

func (s *Service) LinkContrib(ctx context.Context, db pgx.Tx, link ContributorScript) error {
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

func (s *Service) LinkedTags(ctx context.Context, db pgx.Tx) ([]uuid.UUID, error) {
	repo := script.New(db)
	db_tags, err := repo.LinkedTags(ctx)
	if err != nil {
		return nil, err
	}

	tags := make([]uuid.UUID, len(db_tags))
	for i, t := range db_tags {
		tags[i] = t.Bytes
	}

	return tags, nil
}

func (s *Service) LinkedContributors(ctx context.Context, db pgx.Tx) ([]uuid.UUID, error) {
	repo := script.New(db)
	db_contribs, err := repo.LinkedContributors(ctx)
	if err != nil {
		return nil, err
	}

	contribs := make([]uuid.UUID, len(db_contribs))
	for i, t := range db_contribs {
		contribs[i] = t.Bytes
	}

	return contribs, nil
}

func (s *Service) Languages(ctx context.Context, db pgx.Tx) ([]uuid.UUID, error) {
	repo := script.New(db)
	db_langs, err := repo.Languages(ctx)
	if err != nil {
		return nil, err
	}
	langs := make([]uuid.UUID, len(db_langs))
	for i, l := range db_langs {
		langs[i] = l.Bytes
	}
	return langs, nil
}

func (s *Service) DeleteScripts(ctx context.Context, db pgx.Tx, timestamp time.Time) error {
	repo := script.New(db)
	createdAt := pgtype.Timestamptz{Time: timestamp, Valid: true}
	if err := repo.Delete(ctx, createdAt); err != nil {
		return err
	}
	return nil
}
